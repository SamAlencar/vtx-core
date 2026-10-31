"""Funções de domínio para tool-calling da IA (VTX-146).

A IA não escreve script: escolhe uma função do catálogo e manda parâmetros JSON.
`chamar()` valida contra o JSON Schema (jsonschema, MIT), aplica regras de domínio
e devolve sempre {"ok": True, "resultado": ...} ou {"ok": False, "erro": {...}}.
Medidas de entrada em milímetro (como no Revit e nos itens tek TM-262). A API do IfcOpenShell
recebe metro (SI) e converte para a unidade do arquivo; entidade criada crua (perfil) e leitura
de geometria usam a unidade do arquivo, por isso o fator `calculate_unit_scale`.
"""
from __future__ import annotations

import numpy as np
import ifcopenshell.api.feature
import ifcopenshell.api.geometry
import ifcopenshell.api.profile
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.util.element
import ifcopenshell.util.placement
import ifcopenshell.util.unit
import jsonschema

import receitas

VERSAO_ESQUEMA = "0.1.0"
MM = 0.001
_pos = {"type": "number", "exclusiveMinimum": 0, "maximum": 100000}
_coord = {"type": "number", "minimum": -1e6, "maximum": 1e6}


class ErroDominio(Exception):
    def __init__(self, codigo: str, mensagem: str, campo: str | None = None):
        super().__init__(mensagem)
        self.codigo, self.mensagem, self.campo = codigo, mensagem, campo


def _parede(f, a):
    psets = {"Pset_WallCommon": {"IsExternal": a["externa"]}} if "externa" in a else None
    w = receitas.criar_parede(f, a["nome"], a["comprimento_mm"] * MM, a["espessura_mm"] * MM,
                              a["altura_mm"] * MM, psets)
    return {"GlobalId": w.GlobalId}


def _dimensoes_parede(f, w) -> tuple[float, float]:
    """Comprimento (X) e altura (Z) em metro, lidos da extrusão do Body."""
    k = ifcopenshell.util.unit.calculate_unit_scale(f)  # unidade do arquivo -> metro
    for rep in w.Representation.Representations:
        for item in rep.Items:
            if item.is_a("IfcExtrudedAreaSolid"):
                area = item.SweptArea
                pts = area.OuterCurve.Points.CoordList if area.is_a("IfcArbitraryClosedProfileDef") else None
                if pts:
                    xs = [p[0] for p in pts]
                    return (max(xs) - min(xs)) * k, item.Depth * k
    raise ErroDominio("REGRA_VIOLADA", "parede sem extrusão simples; abra o vão manualmente", "parede")


def _vao(f, a):
    try:
        w = f.by_guid(a["parede"])
    except RuntimeError:
        w = None
    if w is None or not w.is_a("IfcWall"):
        raise ErroDominio("ELEMENTO_NAO_ENCONTRADO", f"parede {a['parede']} não existe", "parede")
    comp, alt = _dimensoes_parede(f, w)
    x0, x1 = a["posicao_mm"] * MM, (a["posicao_mm"] + a["largura_mm"]) * MM
    z1 = (a["peitoril_mm"] + a["altura_mm"]) * MM
    if x1 > comp + 1e-9:
        raise ErroDominio("REGRA_VIOLADA", f"vão termina em {x1:.3f} m, parede tem {comp:.3f} m", "posicao_mm")
    if z1 > alt + 1e-9:
        raise ErroDominio("REGRA_VIOLADA", f"vão sobe até {z1:.3f} m, parede tem {alt:.3f} m", "altura_mm")
    vao = ifcopenshell.api.root.create_entity(f, ifc_class="IfcOpeningElement", name="Vão")
    r = ifcopenshell.api.geometry.add_wall_representation(
        f, context=receitas._contexto_body(f), length=a["largura_mm"] * MM, height=a["altura_mm"] * MM,
        thickness=1.0, offset=-0.5)  # atravessa a parede com folga
    ifcopenshell.api.geometry.assign_representation(f, product=vao, representation=r)
    m = ifcopenshell.util.placement.get_local_placement(w.ObjectPlacement) @ np.array(
        [[1, 0, 0, x0], [0, 1, 0, 0], [0, 0, 1, a["peitoril_mm"] * MM], [0, 0, 0, 1]], dtype=float)
    ifcopenshell.api.geometry.edit_object_placement(f, product=vao, matrix=m)
    ifcopenshell.api.feature.add_feature(f, feature=vao, element=w)
    return {"GlobalId": vao.GlobalId, "parede": w.GlobalId}


def _pilar(f, a):
    p = ifcopenshell.api.root.create_entity(f, ifc_class="IfcColumn", name=a["nome"])
    k = ifcopenshell.util.unit.calculate_unit_scale(f)  # entidade crua: unidade do arquivo
    perfil = f.create_entity("IfcRectangleProfileDef", ProfileType="AREA",
                             XDim=a["largura_mm"] * MM / k, YDim=a["profundidade_mm"] * MM / k)
    r = ifcopenshell.api.geometry.add_profile_representation(
        f, context=receitas._contexto_body(f), profile=perfil, depth=a["altura_mm"] * MM)
    ifcopenshell.api.geometry.assign_representation(f, product=p, representation=r)
    m = np.eye(4)
    m[0, 3], m[1, 3] = a["x_mm"] * MM, a["y_mm"] * MM
    ifcopenshell.api.geometry.edit_object_placement(f, product=p, matrix=m)
    ifcopenshell.api.spatial.assign_container(f, products=[p], relating_structure=f.by_type("IfcBuildingStorey")[0])
    return {"GlobalId": p.GlobalId}


def _obj(props: dict, obrig: list[str]) -> dict:
    return {"type": "object", "properties": props, "required": obrig, "additionalProperties": False}


FUNCOES = {
    "criar_parede": {
        "descricao": "Cria parede reta no pavimento térreo, origem (0,0), ao longo de X.",
        "schema": _obj({"nome": {"type": "string", "minLength": 1, "maxLength": 80}, "comprimento_mm": _pos,
                        "espessura_mm": _pos, "altura_mm": _pos, "externa": {"type": "boolean"}},
                       ["nome", "comprimento_mm", "espessura_mm", "altura_mm"]),
        "executar": _parede,
    },
    "abrir_vao": {
        "descricao": "Abre vão (porta/janela) numa parede existente, medido do início da parede.",
        "schema": _obj({"parede": {"type": "string", "pattern": "^[0-9A-Za-z_$]{22}$"}, "largura_mm": _pos,
                        "altura_mm": _pos, "peitoril_mm": {"type": "number", "minimum": 0},
                        "posicao_mm": {"type": "number", "minimum": 0}},
                       ["parede", "largura_mm", "altura_mm", "peitoril_mm", "posicao_mm"]),
        "executar": _vao,
    },
    "lancar_pilar": {
        "descricao": "Lança pilar retangular no pavimento térreo, centrado em (x, y).",
        "schema": _obj({"nome": {"type": "string", "minLength": 1, "maxLength": 80}, "largura_mm": _pos,
                        "profundidade_mm": _pos, "altura_mm": _pos, "x_mm": _coord, "y_mm": _coord},
                       ["nome", "largura_mm", "profundidade_mm", "altura_mm", "x_mm", "y_mm"]),
        "executar": _pilar,
    },
}


def ferramentas() -> list[dict]:
    """Catálogo no formato de tool-calling (name/description/input_schema) para a API da IA."""
    return [{"name": n, "description": d["descricao"], "input_schema": d["schema"],
             "x-versao-esquema": VERSAO_ESQUEMA} for n, d in FUNCOES.items()]


def _erro(codigo, mensagem, campo=None):
    return {"ok": False, "erro": {"codigo": codigo, "campo": campo, "mensagem": mensagem}}


def chamar(f, nome: str, args: dict) -> dict:
    """Único ponto de entrada da IA. Nunca lança exceção para o chamador."""
    if nome not in FUNCOES:
        return _erro("FUNCAO_DESCONHECIDA", f"função '{nome}' não existe; use ferramentas()")
    v = jsonschema.Draft202012Validator(FUNCOES[nome]["schema"])
    falhas = sorted(v.iter_errors(args), key=lambda e: list(e.path))
    if falhas:
        e = falhas[0]
        campo = e.path[0] if e.path else (e.message.split("'")[1] if "'" in e.message else None)
        return _erro("PARAMETRO_INVALIDO", e.message, campo)
    try:
        return {"ok": True, "resultado": FUNCOES[nome]["executar"](f, args)}
    except ErroDominio as e:
        return _erro(e.codigo, e.mensagem, e.campo)
    except Exception as e:  # falha interna: registra, não vaza stack para a IA
        return _erro("ERRO_INTERNO", f"{type(e).__name__}: {e}")
