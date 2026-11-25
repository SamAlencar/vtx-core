#!/usr/bin/env python3
"""Valida o backlog (schema, entregável das concluídas) e o INDEX da base de conhecimento.

Uso: python scripts/validar_backlog.py [dir_backlog]
Sai com código 1 e uma linha por erro se houver problema.
"""
from __future__ import annotations

import glob
import os
import re
import sys

import yaml

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backlog_lib import STATUS_VALIDOS, carregar  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RE_ID = re.compile(r"^VTX-\d{3}$")
CHAVES_MESTRE = {"id", "titulo", "fase", "area", "prioridade", "status"}
CHAVES_DIA = {"id", "titulo", "area", "status"}
EXTENSOES_CAMINHO = {".md", ".mdc", ".py", ".yml", ".yaml", ".sh", ".json", ".html", ".css"}


def _caminhos_entregavel(texto: str) -> list[str]:
    if not texto or not str(texto).strip():
        return []
    partes = [p.strip() for p in str(texto).replace(" e ", " + ").split("+")]
    caminhos = []
    for parte in partes:
        if not parte:
            continue
        token = parte.split()[0].rstrip(",")
        if token.startswith("`") and token.endswith("`"):
            token = token[1:-1]
        if "/" in token or os.path.splitext(token)[1] in EXTENSOES_CAMINHO:
            caminhos.append(token)
    return caminhos


def _docs_knowledge(raiz: str) -> list[str]:
    base = os.path.join(raiz, "knowledge")
    docs = []
    for caminho in glob.glob(os.path.join(base, "**", "*.md"), recursive=True):
        rel = os.path.relpath(caminho, base).replace("\\", "/")
        if rel in {"INDEX.md", "ROADMAP.md"}:
            continue
        # Modelos internos já cobertos pelo README da pasta no INDEX.
        if rel.startswith("templates/memoria-projeto/") and not rel.endswith("README.md"):
            continue
        docs.append(rel)
    return sorted(docs)


def validar(raiz: str, dir_backlog: str) -> list[str]:
    erros = []
    mestre_path = os.path.join(dir_backlog, "projeto.yaml")
    with open(mestre_path, encoding="utf-8") as fh:
        mestre = yaml.safe_load(fh) or {}
    if not mestre.get("projeto"):
        erros.append("projeto.yaml: falta a chave 'projeto'")
    fases = mestre.get("fases") or []
    ids_fase = {f.get("id") for f in fases}
    for i, fase in enumerate(fases):
        if not fase.get("id") or not fase.get("nome"):
            erros.append(f"projeto.yaml: fase[{i}] precisa de id e nome")

    tarefas = mestre.get("tarefas") or []
    ids = []
    for t in tarefas:
        tid = str(t.get("id") or "")
        ids.append(tid)
        falta = CHAVES_MESTRE - set(t)
        if falta:
            erros.append(f"{tid or '?'}: faltam campos {sorted(falta)}")
            continue
        if not RE_ID.match(tid):
            erros.append(f"{tid}: id fora do padrão VTX-000")
        if t.get("fase") not in ids_fase:
            erros.append(f"{tid}: fase {t.get('fase')!r} não está em fases")
        try:
            int(t["prioridade"])
        except (TypeError, ValueError):
            erros.append(f"{tid}: prioridade não é inteiro")
        if t.get("status") not in STATUS_VALIDOS:
            erros.append(f"{tid}: status {t.get('status')!r} inválido")
        for dep in t.get("depende_de") or []:
            if dep not in {x.get("id") for x in tarefas}:
                erros.append(f"{tid}: depende_de {dep} não existe")
    if len(ids) != len(set(ids)):
        erros.append("projeto.yaml: há ids repetidos")

    for caminho in sorted(glob.glob(os.path.join(dir_backlog, "[0-9]" * 4 + "-[0-9]" * 2 + "-[0-9]" * 2 + ".yaml"))):
        with open(caminho, encoding="utf-8") as fh:
            doc = yaml.safe_load(fh) or {}
        if not doc.get("data"):
            erros.append(f"{os.path.basename(caminho)}: falta 'data'")
        for t in doc.get("tarefas") or []:
            tid = str(t.get("id") or os.path.basename(caminho))
            falta = CHAVES_DIA - set(t)
            if falta:
                erros.append(f"{os.path.basename(caminho)} {tid}: faltam campos públicos {sorted(falta)}")
            if t.get("status") not in STATUS_VALIDOS:
                erros.append(f"{os.path.basename(caminho)} {tid}: status {t.get('status')!r} inválido")

    projeto, _ = carregar(dir_backlog)
    for t in projeto.get("tarefas", []):
        if t.get("status") != "concluído":
            continue
        if t.get("fase") == "F0":
            continue
        caminhos = _caminhos_entregavel(t.get("entregavel") or "")
        if not caminhos:
            erros.append(f"{t['id']}: concluída sem entregável verificável")
            continue
        for rel in caminhos:
            if not os.path.exists(os.path.join(raiz, rel)):
                erros.append(f"{t['id']}: entregável ausente: {rel}")

    index = os.path.join(raiz, "knowledge", "INDEX.md")
    texto_index = ""
    if os.path.exists(index):
        with open(index, encoding="utf-8") as fh:
            texto_index = fh.read()
    for rel in _docs_knowledge(raiz):
        if rel not in texto_index:
            erros.append(f"knowledge/{rel} não aparece no INDEX.md")
    return erros


def main(argv=None) -> int:
    argv = list(argv or sys.argv[1:])
    dir_backlog = os.path.abspath(argv[0] if argv else os.path.join(RAIZ, "backlog"))
    erros = validar(RAIZ, dir_backlog)
    if erros:
        print("\n".join(erros))
        return 1
    print("Backlog e INDEX válidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
