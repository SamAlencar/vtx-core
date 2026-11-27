"""Receitas IfcOpenShell 0.9 para agentes VTX (skill ifc-python, VTX-145).

Funções pequenas e determinísticas: criar modelo e parede, listar elementos,
ler/gravar Psets, validar contra IDS (ifctester) e diff por GlobalId.
IfcOpenShell e ifctester (LGPL-3.0) são usados como biblioteca, sem modificar.
"""
from __future__ import annotations

from typing import Literal

import ifcopenshell
import ifcopenshell.api.aggregate
import ifcopenshell.api.context
import ifcopenshell.api.geometry
import ifcopenshell.api.project
import ifcopenshell.api.pset
import ifcopenshell.api.root
import ifcopenshell.api.spatial
import ifcopenshell.api.unit
import ifcopenshell.util.element


def criar_modelo(schema: Literal["IFC2X3", "IFC4", "IFC4X3"] = "IFC4", nome: str = "Projeto") -> ifcopenshell.file:
    """IFC novo com projeto, unidades padrão do IfcOpenShell (mm, m², m³), contexto Body e Site/Edifício/Pavimento.

    A API (`ifcopenshell.api.*`) recebe medidas em metro e converte para mm no arquivo.
    """
    f = ifcopenshell.api.project.create_file(version=schema)
    projeto = ifcopenshell.api.root.create_entity(f, ifc_class="IfcProject", name=nome)
    ifcopenshell.api.unit.assign_unit(f)  # padrão: milímetro, m², m³
    modelo = ifcopenshell.api.context.add_context(f, context_type="Model")
    ifcopenshell.api.context.add_context(
        f, context_type="Model", context_identifier="Body", target_view="MODEL_VIEW", parent=modelo
    )
    pai = projeto
    for classe, n in (("IfcSite", "Terreno"), ("IfcBuilding", "Edificio"), ("IfcBuildingStorey", "Terreo")):
        filho = ifcopenshell.api.root.create_entity(f, ifc_class=classe, name=n)
        ifcopenshell.api.aggregate.assign_object(f, products=[filho], relating_object=pai)
        pai = filho
    return f


def _contexto_body(f):
    for c in f.by_type("IfcGeometricRepresentationSubContext"):
        if c.ContextIdentifier == "Body":
            return c
    raise ValueError("modelo sem contexto Body; use criar_modelo()")


def definir_pset(f, elemento, psets: dict) -> None:
    """Cria ou edita Psets: {"Pset_WallCommon": {"IsExternal": True}}."""
    existentes = ifcopenshell.util.element.get_psets(elemento)
    for nome, props in psets.items():
        if nome in existentes:
            pset = f.by_id(existentes[nome]["id"])
        else:
            pset = ifcopenshell.api.pset.add_pset(f, product=elemento, name=nome)
        ifcopenshell.api.pset.edit_pset(f, pset=pset, properties=props)


def criar_parede(f, nome: str, comprimento: float, espessura: float, altura: float,
                 psets: dict | None = None):
    """IfcWall reta no eixo X do primeiro pavimento, medidas em metro (> 0)."""
    for rotulo, v in (("comprimento", comprimento), ("espessura", espessura), ("altura", altura)):
        if not v or v <= 0:
            raise ValueError(f"{rotulo} deve ser > 0 (recebido {v!r})")
    parede = ifcopenshell.api.root.create_entity(f, ifc_class="IfcWall", name=nome)
    rep = ifcopenshell.api.geometry.add_wall_representation(
        f, context=_contexto_body(f), length=comprimento, height=altura, thickness=espessura
    )
    ifcopenshell.api.geometry.assign_representation(f, product=parede, representation=rep)
    ifcopenshell.api.geometry.edit_object_placement(f, product=parede)
    pavimento = f.by_type("IfcBuildingStorey")[0]
    ifcopenshell.api.spatial.assign_container(f, products=[parede], relating_structure=pavimento)
    if psets:
        definir_pset(f, parede, psets)
    return parede


def listar(f, classe: str = "IfcElement") -> list[dict]:
    """Elementos da classe (com subclasses), em qualquer esquema (IFC2X3/IFC4/IFC4X3)."""
    return [{"GlobalId": e.GlobalId, "classe": e.is_a(), "nome": e.Name} for e in f.by_type(classe)]


def ler_psets(elemento) -> dict:
    """Psets e Qtos do elemento (herdados do tipo incluídos), sem a chave interna 'id'."""
    return {n: {k: v for k, v in p.items() if k != "id"}
            for n, p in ifcopenshell.util.element.get_psets(elemento).items()}


def validar_ids(caminho_ifc, caminho_ids) -> dict:
    """Valida o IFC contra um arquivo IDS 1.0; devolve resumo JSON-serializável."""
    from ifctester import ids, reporter  # type: ignore[import-untyped]

    regras = ids.open(str(caminho_ids))
    modelo = ifcopenshell.open(str(caminho_ifc))  # manter vivo até o report (senão "Instance #n not found")
    regras.validate(modelo)
    rel = reporter.Json(regras).report()
    especs = [{"nome": s["name"], "aprovado": s["status"],
               "falhas": [fl.get("reason") for r in s.get("requirements", []) for fl in r.get("failed_entities", [])]}
              for s in rel["specifications"]]
    return {"aprovado": bool(rel["status"]), "especificacoes": especs}


def _assinatura(e) -> tuple:
    return (e.is_a(), e.Name, repr(sorted(ler_psets(e).items())))


def diff_por_globalid(a, b, classe: str = "IfcElement") -> dict:
    """Diff semântico simples entre duas versões: identidade = GlobalId.

    'alterados' compara classe, nome e Psets (não geometria). Se o exportador
    regerar GlobalId, tudo aparece como removido + adicionado (ver VTX-151).
    """
    ea = {e.GlobalId: e for e in a.by_type(classe)}
    eb = {e.GlobalId: e for e in b.by_type(classe)}
    return {
        "adicionados": [{"GlobalId": g, "classe": eb[g].is_a(), "nome": eb[g].Name} for g in eb.keys() - ea.keys()],
        "removidos": [{"GlobalId": g, "classe": ea[g].is_a(), "nome": ea[g].Name} for g in ea.keys() - eb.keys()],
        "alterados": [{"GlobalId": g, "classe": eb[g].is_a(), "nome": eb[g].Name}
                      for g in ea.keys() & eb.keys() if _assinatura(ea[g]) != _assinatura(eb[g])],
    }
