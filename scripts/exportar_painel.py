#!/usr/bin/env python3
"""Exporta o backlog para o painel público, SOMENTE com campos sanitizados.

Uso: python scripts/exportar_painel.py <dir_backlog> <arquivo_saida.json>
Campos exportados: data, id, titulo, area, status. Todo o resto é descartado.
"""
import glob
import json
import os
import sys
from datetime import datetime, timezone

import yaml

STATUS_VALIDOS = {"a fazer", "em andamento", "concluído"}


def main(dir_backlog: str, saida: str) -> None:
    dias = []
    for caminho in sorted(glob.glob(os.path.join(dir_backlog, "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].yaml"))):
        with open(caminho, encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
        data = str(doc.get("data") or os.path.basename(caminho)[:10])
        tarefas = []
        for t in doc.get("tarefas") or []:
            status = str(t.get("status", "")).strip().lower()
            if status not in STATUS_VALIDOS:
                status = "a fazer"
            tarefas.append({
                "id": str(t.get("id", "")),
                "titulo": str(t.get("titulo", "")),
                "area": str(t.get("area", "")),
                "status": status,
            })
        dias.append({"data": data, "tarefas": tarefas})
    dias.sort(key=lambda d: d["data"], reverse=True)
    out = {"gerado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"), "dias": dias}
    os.makedirs(os.path.dirname(saida) or ".", exist_ok=True)
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"Exportados {len(dias)} dia(s) para {saida}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
