#!/usr/bin/env python3
"""Rotina diária: mostra a próxima tarefa do projeto (em andamento primeiro, senão a fazer de menor prioridade).

Uso: python scripts/proxima_tarefa.py [dir_backlog]

Ignora tarefas canceladas e aguardando, e as que têm depende_de ainda não concluída. O progresso é concluídas / (total - canceladas).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backlog_lib import carregar


def _deps_ok(t, por_id):
    """Uma tarefa só entra na fila quando todas as depende_de estão concluídas."""
    for dep in t.get("depende_de") or []:
        d = por_id.get(dep)
        if not d or d.get("status") != "concluído":
            return False
    return True


projeto, _ = carregar(sys.argv[1] if len(sys.argv) > 1 else "backlog")
ts = sorted(projeto.get("tarefas", []), key=lambda t: int(t["prioridade"]))
por_id = {t["id"]: t for t in ts}
ativos = [t for t in ts if t["status"] != "cancelado"]
prox = next((t for t in ts if t["status"] == "em andamento" and _deps_ok(t, por_id)), None) or next(
    (t for t in ts if t["status"] == "a fazer" and _deps_ok(t, por_id)), None
)
feitas = sum(t["status"] == "concluído" for t in ativos)
print(f"Progresso: {feitas}/{len(ativos)} ({round(100 * feitas / len(ativos)) if ativos else 0}%)")
if prox:
    print(f"Próxima: {prox['id']} [{prox['fase']}] {prox['titulo']} -> {prox.get('entregavel', '')}")
else:
    print("Projeto concluído.")
