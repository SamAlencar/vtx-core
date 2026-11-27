#!/usr/bin/env python3
"""Exporta o backlog para JSON, SOMENTE com campos sanitizados.

Uso: python scripts/exportar_painel.py <dir_backlog> <arquivo_saida.json>
Projeto: id, titulo, fase, area, prioridade, status. Dias: data, id, titulo, area, status.
Notas, responsáveis e entregáveis (caminhos) NUNCA são exportados.

O painel público (SamAlencar/painel-central) se atualiza sozinho a partir da API;
este script é um helper local e não publica o site (VTX-171).
"""
import json
import os
import sys
from datetime import UTC, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backlog_lib import _status, carregar


def main(dir_backlog, saida):
    projeto, dias = carregar(dir_backlog)
    out = {
        "gerado_em": datetime.now(UTC).isoformat(timespec="seconds"),
        "projeto": {
            "nome": str(projeto.get("projeto", "")),
            "fases": [{"id": str(f["id"]), "nome": str(f["nome"])} for f in projeto.get("fases", [])],
            "tarefas": [
                {k: (int(t[k]) if k == "prioridade" else str(t[k])) for k in ("id", "titulo", "fase", "area", "prioridade", "status")}
                for t in sorted(projeto.get("tarefas", []), key=lambda t: int(t["prioridade"]))
            ],
        },
        "dias": [
            {"data": d["data"], "tarefas": [
                {"id": str(t.get("id", "")), "titulo": str(t.get("titulo", "")),
                 "area": str(t.get("area", "")), "status": _status(t.get("status"))}
                for t in d["tarefas"]]}
            for d in sorted(dias, key=lambda d: d["data"], reverse=True)
        ],
    }
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Exportados {len(out['projeto']['tarefas'])} tarefas do projeto e {len(dias)} dia(s) para {saida}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
