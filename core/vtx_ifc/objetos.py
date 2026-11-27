"""Camada de objetos IFC <-> JSON (VTX-152, parte 1).

O IFC aprovado de cada versão é a fonte da verdade (versionamento-ifc.md §7.1).
`extrair` gera um objeto JSON por elemento (vai para Postgres jsonb e para a IA);
`aplicar` devolve ao IFC base só o que mudou, preservando GlobalId e o resto do
arquivo (geometria, relações não tocadas). Editáveis: nome, psets (da instância),
andar, grupos e tipo. Somente leitura: classe, materiais, qtos.
"""
from __future__ import annotations

import ifcopenshell
import ifcopenshell.api.group
import ifcopenshell.api.pset
import ifcopenshell.api.spatial
import ifcopenshell.api.type
import ifcopenshell.util.element as ue

EDITAVEIS = ("nome", "psets", "andar", "grupos", "tipo")
SOMENTE_LEITURA = ("classe", "materiais", "qtos")


def _json(v):
    if isinstance(v, (tuple, list)):
        return [_json(x) for x in v]
    if isinstance(v, (bool, int, float, str)) or v is None:
        return v
    return str(v)


def _ref(e):
    return {"globalid": e.GlobalId, "nome": e.Name} if e is not None else None


def _materiais(e) -> list[str]:
    m = ue.get_material(e, should_inherit=True)
    if m is None:
        return []
    if m.is_a("IfcMaterialLayerSetUsage"):
        m = m.ForLayerSet
    for attr, filho in (("MaterialLayers", "Material"), ("MaterialConstituents", "Material"),
                        ("MaterialProfiles", "Material")):
        if hasattr(m, attr):
            return [mat.Name for x in getattr(m, attr) if (mat := getattr(x, filho))]
    if m.is_a("IfcMaterialList"):
        return [x.Name for x in m.Materials]
    return [m.Name] if m.is_a("IfcMaterial") else []


def _grupos(e) -> list[dict]:
    rels = [r for r in getattr(e, "HasAssignments", []) or [] if r.is_a("IfcRelAssignsToGroup")]
    return sorted((_ref(r.RelatingGroup) for r in rels), key=lambda g: g["globalid"])


def _objeto(e) -> dict:
    def proprios(**k):
        return {n: {p: _json(v) for p, v in d.items() if p != "id"}
                for n, d in ue.get_psets(e, should_inherit=False, **k).items()}
    return {
        "globalid": e.GlobalId, "classe": e.is_a(), "nome": e.Name,
        "tipo": _ref(ue.get_type(e)) if not e.is_a("IfcTypeObject") else None,
        "psets": proprios(psets_only=True), "qtos": proprios(qtos_only=True),
        "materiais": _materiais(e),
        "andar": _ref(ue.get_container(e)) if not e.is_a("IfcTypeObject") else None,
        "grupos": _grupos(e),
    }


def extrair(f, classe: str = "IfcElement") -> list[dict]:
    """Um objeto JSON-serializável por entidade da classe, ordenado por GlobalId."""
    return sorted((_objeto(e) for e in f.by_type(classe)), key=lambda o: o["globalid"])


def _erro(gid, codigo, msg):
    return {"globalid": gid, "codigo": codigo, "mensagem": msg}


def _por_gid(f, ref, classe):
    try:
        e = f.by_guid(ref["globalid"])
    except (RuntimeError, KeyError, TypeError):
        return None
    return e if e.is_a(classe) else None


def aplicar(f, objetos: list[dict]) -> dict:
    """Aplica no IFC `f` (muta) as diferenças dos objetos. Nunca cria elemento; nunca lança."""
    alterados, erros = 0, []
    for obj in objetos:
        gid = obj.get("globalid")
        try:
            e = f.by_guid(gid)
        except (RuntimeError, TypeError):
            erros.append(_erro(gid, "globalid_inexistente", "GlobalId não existe no IFC base"))
            continue
        atual, mudou = _objeto(e), False
        for campo in SOMENTE_LEITURA:
            if campo in obj and obj[campo] != atual[campo]:
                erros.append(_erro(gid, "campo_somente_leitura", f"'{campo}' não é editável nesta camada"))
        if "nome" in obj and obj["nome"] != atual["nome"]:
            e.Name, mudou = obj["nome"], True
        if "psets" in obj and obj["psets"] != atual["psets"]:
            existentes = ue.get_psets(e, should_inherit=False, psets_only=True)
            for nome, props in obj["psets"].items():
                velho = atual["psets"].get(nome, {})
                novo = {**{p: None for p in velho if p not in props}, **props}
                if novo == velho:
                    continue
                pset = f.by_id(existentes[nome]["id"]) if nome in existentes else \
                    ifcopenshell.api.pset.add_pset(f, product=e, name=nome)
                ifcopenshell.api.pset.edit_pset(f, pset=pset, properties=novo)
            mudou = True
        if obj.get("andar") and (atual["andar"] or {}).get("globalid") != obj["andar"]["globalid"]:
            s = _por_gid(f, obj["andar"], "IfcSpatialElement")
            if s is None:
                erros.append(_erro(gid, "referencia_invalida", "andar não encontrado"))
            else:
                ifcopenshell.api.spatial.assign_container(f, products=[e], relating_structure=s)
                mudou = True
        if "grupos" in obj:
            novos = {g["globalid"] for g in obj["grupos"]}
            velhos = {g["globalid"] for g in atual["grupos"]}
            for g in velhos - novos:
                ifcopenshell.api.group.unassign_group(f, products=[e], group=f.by_guid(g))
            for g in novos - velhos:
                grp = _por_gid(f, {"globalid": g}, "IfcGroup")
                if grp is None:
                    erros.append(_erro(gid, "referencia_invalida", f"grupo {g} não encontrado"))
                else:
                    ifcopenshell.api.group.assign_group(f, products=[e], group=grp)
            mudou |= novos != velhos
        if obj.get("tipo") and (atual["tipo"] or {}).get("globalid") != obj["tipo"]["globalid"]:
            t = _por_gid(f, obj["tipo"], "IfcTypeObject")
            if t is None:
                erros.append(_erro(gid, "referencia_invalida", "tipo não encontrado"))
            else:
                ifcopenshell.api.type.assign_type(f, related_objects=[e], relating_type=t)
                mudou = True
        alterados += mudou
    return {"alterados": alterados, "erros": erros}
