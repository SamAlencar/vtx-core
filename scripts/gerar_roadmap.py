#!/usr/bin/env python3
"""Gera knowledge/ROADMAP.md a partir de backlog/projeto.yaml (tarefas pendentes do plano, por fase e prioridade)."""
import yaml

doc = yaml.safe_load(open("backlog/projeto.yaml", encoding="utf-8"))
nomes = {f["id"]: f["nome"] for f in doc["fases"]}
ts = sorted([t for t in doc["tarefas"] if t["fase"] != "F0"], key=lambda t: t["prioridade"])
out = ["# Roadmap da Base de Conhecimento", "",
       "Gerado por `scripts/gerar_roadmap.py` a partir de `backlog/projeto.yaml` (fonte da verdade).",
       "Uma tarefa por sessão diária, em ordem de prioridade. Próxima: `python scripts/proxima_tarefa.py`.",
       "Ao concluir um documento, adicioná-lo ao `INDEX.md`.", ""]
cur = None
for i, t in enumerate(ts, 1):
    if t["fase"] != cur:
        cur = t["fase"]
        out += ["", f"## {cur} — {nomes[cur]}", ""]
    out.append(f"{i}. **{t['id']}** {t['titulo']} → `{t.get('entregavel', '')}`")
open("knowledge/ROADMAP.md", "w", encoding="utf-8").write("\n".join(out) + "\n")
print(f"ROADMAP com {len(ts)} tarefas")
