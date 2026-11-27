#!/usr/bin/env python3
"""Gera knowledge/ROADMAP.md a partir do backlog (tarefas ainda não concluídas nem canceladas, por fase e prioridade).

Usa o status efetivo (diário mais recente, senão o mestre). Uso: python scripts/gerar_roadmap.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backlog_lib import carregar

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
projeto, _ = carregar(os.path.join(RAIZ, "backlog"))
nomes = {f["id"]: f["nome"] for f in projeto.get("fases", [])}
excluidos = {"concluído", "cancelado"}
ts = sorted(
    [t for t in projeto.get("tarefas", []) if t.get("fase") != "F0" and t.get("status") not in excluidos],
    key=lambda t: int(t["prioridade"]),
)
out = [
    "# Roadmap da Base de Conhecimento",
    "",
    "Gerado por `scripts/gerar_roadmap.py` a partir do status efetivo do backlog (mestre + diários).",
    "Só entram tarefas ainda não concluídas nem canceladas, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.",
    "Ao concluir um documento, adicioná-lo ao `INDEX.md`.",
]
cur = None
for i, t in enumerate(ts, 1):
    if t["fase"] != cur:
        cur = t["fase"]
        out += ["", f"## {cur} — {nomes.get(cur, cur)}", ""]
    out.append(f"{i}. **{t['id']}** {t['titulo']} → `{t.get('entregavel', '')}`")
caminho = os.path.join(RAIZ, "knowledge/ROADMAP.md")
with open(caminho, "w", encoding="utf-8") as fh:
    fh.write("\n".join(out) + "\n")
print(f"ROADMAP com {len(ts)} tarefas pendentes")
