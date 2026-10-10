"""Leitura e consolidação do backlog (mestre + diários)."""
import glob
import os

import yaml

STATUS_VALIDOS = {"a fazer", "em andamento", "concluído"}
PADRAO_DIA = "[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9].yaml"


def _status(v):
    s = str(v or "").strip().lower()
    return s if s in STATUS_VALIDOS else "a fazer"


def carregar(dir_backlog):
    """Retorna (projeto, dias). O status de cada tarefa do projeto é o do diário mais recente que a cita."""
    dias = []
    for caminho in sorted(glob.glob(os.path.join(dir_backlog, PADRAO_DIA))):
        with open(caminho, encoding="utf-8") as f:
            doc = yaml.safe_load(f) or {}
        data = str(doc.get("data") or os.path.basename(caminho)[:10])
        dias.append({"data": data, "tarefas": doc.get("tarefas") or []})
    dias.sort(key=lambda d: d["data"])

    projeto = {"projeto": "", "fases": [], "tarefas": []}
    mestre = os.path.join(dir_backlog, "projeto.yaml")
    if os.path.exists(mestre):
        with open(mestre, encoding="utf-8") as f:
            projeto = yaml.safe_load(f) or projeto
    idx = {t["id"]: t for t in projeto.get("tarefas", [])}
    for dia in dias:  # ordem cronológica: o mais recente prevalece
        for t in dia["tarefas"]:
            if t.get("id") in idx:
                idx[t["id"]]["status"] = t.get("status")
    for t in projeto.get("tarefas", []):
        t["status"] = _status(t.get("status"))
    return projeto, dias
