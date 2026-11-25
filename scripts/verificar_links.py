#!/usr/bin/env python3
"""Confere links relativos em arquivos Markdown do repositório.

Uso: python scripts/verificar_links.py [raiz]
Sai com código 1 e uma linha por link quebrado.
"""
from __future__ import annotations

import os
import re
import sys

RE_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _eh_externo(url: str) -> bool:
    u = url.lower()
    return u.startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def verificar(raiz: str) -> list[str]:
    erros = []
    raiz = os.path.abspath(raiz)
    for dirpath, dirnames, arquivos in os.walk(raiz):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules", "__pycache__", ".venv", "dist", "build"}]
        for nome in arquivos:
            if not nome.endswith(".md"):
                continue
            caminho = os.path.join(dirpath, nome)
            rel_doc = os.path.relpath(caminho, raiz).replace("\\", "/")
            with open(caminho, encoding="utf-8") as fh:
                texto = fh.read()
            for bruto in RE_LINK.findall(texto):
                url = bruto.split()[0].strip()
                if not url or url.startswith("#") or _eh_externo(url):
                    continue
                url = url.split("#", 1)[0]
                if not url:
                    continue
                alvo = os.path.normpath(os.path.join(os.path.dirname(caminho), url))
                if not os.path.exists(alvo):
                    erros.append(f"{rel_doc}: link quebrado {url}")
    return erros


def main(argv=None) -> int:
    argv = list(argv or sys.argv[1:])
    raiz = os.path.abspath(argv[0] if argv else os.path.join(os.path.dirname(__file__), ".."))
    erros = verificar(raiz)
    if erros:
        print("\n".join(erros))
        return 1
    print("Links relativos ok.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
