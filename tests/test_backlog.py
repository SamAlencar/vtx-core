"""Testes dos scripts do backlog: exportação sanitizada e status efetivo."""
import json
import os
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(RAIZ, "scripts"))

import exportar_painel
from backlog_lib import carregar

CHAVES_PROIBIDAS = ("notas", "responsavel", "entregavel", "depende_de")
CHAVES_TAREFA_PROJETO = {"id", "titulo", "fase", "area", "prioridade", "status"}
CHAVES_TAREFA_DIA = {"id", "titulo", "area", "status"}


def gravar_yaml(pasta, nome, documento):
    caminho = os.path.join(pasta, nome)
    with open(caminho, "w", encoding="utf-8") as arquivo:
        yaml.safe_dump(documento, arquivo, allow_unicode=True, sort_keys=False)
    return caminho


def coletar_chaves(valor, achadas=None):
    if achadas is None:
        achadas = set()
    if isinstance(valor, dict):
        achadas.update(valor.keys())
        for item in valor.values():
            coletar_chaves(item, achadas)
    elif isinstance(valor, list):
        for item in valor:
            coletar_chaves(item, achadas)
    return achadas


def exportar(dir_backlog, saida):
    with redirect_stdout(StringIO()):
        exportar_painel.main(dir_backlog, saida)
    with open(saida, encoding="utf-8") as arquivo:
        texto = arquivo.read()
    return json.loads(texto), texto


class TestExportarPainel(unittest.TestCase):
    def test_json_nao_contem_campos_privados(self):
        sentinelas = {
            "notas_mestre": "PRIVADO-NOTAS-MESTRE-9f3a",
            "entregavel_mestre": "PRIVADO-ENTREGAVEL-MESTRE-9f3a",
            "depende_mestre": "PRIVADO-DEPENDE-MESTRE-9f3a",
            "notas_dia": "PRIVADO-NOTAS-DIA-9f3a",
            "responsavel_dia": "PRIVADO-RESPONSAVEL-9f3a",
            "entregavel_dia": "PRIVADO-ENTREGAVEL-DIA-9f3a",
            "depende_dia": "PRIVADO-DEPENDE-DIA-9f3a",
        }
        with tempfile.TemporaryDirectory() as pasta:
            gravar_yaml(pasta, "projeto.yaml", {
                "projeto": "Projeto de teste",
                "fases": [{"id": "F1", "nome": "Fase de teste"}],
                "tarefas": [
                    {
                        "id": "VTX-900",
                        "titulo": "Tarefa publica",
                        "fase": "F1",
                        "area": "Qualidade",
                        "prioridade": 2,
                        "status": "a fazer",
                        "entregavel": sentinelas["entregavel_mestre"],
                        "depende_de": [sentinelas["depende_mestre"]],
                        "notas": sentinelas["notas_mestre"],
                    },
                    {
                        "id": "VTX-901",
                        "titulo": "Outra tarefa",
                        "fase": "F1",
                        "area": "Gestao",
                        "prioridade": 1,
                        "status": "em andamento",
                        "entregavel": "PRIVADO-ENTREGAVEL-MESTRE-b2c1",
                        "notas": "PRIVADO-NOTAS-MESTRE-b2c1",
                    },
                ],
            })
            gravar_yaml(pasta, "2026-10-01.yaml", {
                "data": "2026-10-01",
                "tarefas": [
                    {
                        "id": "VTX-900",
                        "titulo": "Tarefa no dia",
                        "area": "Qualidade",
                        "status": "concluído",
                        "responsavel": sentinelas["responsavel_dia"],
                        "notas": sentinelas["notas_dia"],
                        "entregavel": sentinelas["entregavel_dia"],
                        "depende_de": [sentinelas["depende_dia"]],
                    }
                ],
            })
            saida = os.path.join(pasta, "painel.json")
            doc, texto = exportar(pasta, saida)

        chaves = coletar_chaves(doc)
        for chave in CHAVES_PROIBIDAS:
            self.assertNotIn(chave, chaves)
            self.assertNotIn(f'"{chave}"', texto)
        for valor in [*sentinelas.values(), "PRIVADO-ENTREGAVEL-MESTRE-b2c1", "PRIVADO-NOTAS-MESTRE-b2c1"]:
            self.assertNotIn(valor, texto)

        tarefas = doc["projeto"]["tarefas"]
        self.assertEqual([t["id"] for t in tarefas], ["VTX-901", "VTX-900"])
        for tarefa in tarefas:
            self.assertEqual(set(tarefa.keys()), CHAVES_TAREFA_PROJETO)
        for dia in doc["dias"]:
            self.assertEqual(set(dia.keys()), {"data", "tarefas"})
            for tarefa in dia["tarefas"]:
                self.assertEqual(set(tarefa.keys()), CHAVES_TAREFA_DIA)


class TestCarregar(unittest.TestCase):
    def test_status_do_diario_mais_recente_prevalece(self):
        with tempfile.TemporaryDirectory() as pasta:
            gravar_yaml(pasta, "projeto.yaml", {
                "projeto": "Projeto status",
                "fases": [{"id": "F1", "nome": "Fase"}],
                "tarefas": [
                    {
                        "id": "VTX-A",
                        "titulo": "Citada em dois diarios",
                        "fase": "F1",
                        "area": "Qualidade",
                        "prioridade": 1,
                        "status": "a fazer",
                    },
                    {
                        "id": "VTX-B",
                        "titulo": "Nao citada",
                        "fase": "F1",
                        "area": "Qualidade",
                        "prioridade": 2,
                        "status": "em andamento",
                    },
                    {
                        "id": "VTX-C",
                        "titulo": "Status invalido no mestre",
                        "fase": "F1",
                        "area": "Qualidade",
                        "prioridade": 3,
                        "status": "concluido",
                    },
                    {
                        "id": "VTX-D",
                        "titulo": "Status invalido no diario recente",
                        "fase": "F1",
                        "area": "Qualidade",
                        "prioridade": 4,
                        "status": "concluído",
                    },
                ],
            })
            gravar_yaml(pasta, "2026-01-01.yaml", {
                "data": "2026-01-01",
                "tarefas": [
                    {"id": "VTX-A", "titulo": "Citada", "area": "Qualidade", "status": "em andamento"},
                    {"id": "VTX-D", "titulo": "Citada", "area": "Qualidade", "status": "em andamento"},
                ],
            })
            gravar_yaml(pasta, "2026-02-01.yaml", {
                "data": "2026-02-01",
                "tarefas": [
                    {"id": "VTX-A", "titulo": "Citada", "area": "Qualidade", "status": "concluído"},
                    {"id": "VTX-D", "titulo": "Citada", "area": "Qualidade", "status": "concluido"},
                ],
            })
            projeto, _dias = carregar(pasta)

        status = {t["id"]: t["status"] for t in projeto["tarefas"]}
        self.assertEqual(status["VTX-A"], "concluído")
        self.assertEqual(status["VTX-B"], "em andamento")
        self.assertEqual(status["VTX-C"], "a fazer")
        self.assertEqual(status["VTX-D"], "a fazer")


class TestFumacaBacklogReal(unittest.TestCase):
    def test_exportacao_do_diretorio_real(self):
        with tempfile.TemporaryDirectory() as pasta:
            saida = os.path.join(pasta, "backlog.json")
            doc, texto = exportar(os.path.join(RAIZ, "backlog"), saida)

        self.assertEqual(set(doc.keys()), {"gerado_em", "projeto", "dias"})
        projeto = doc["projeto"]
        self.assertEqual(set(projeto.keys()), {"nome", "fases", "tarefas"})
        self.assertTrue(projeto["tarefas"])
        self.assertTrue(doc["dias"])
        for fase in projeto["fases"]:
            self.assertEqual(set(fase.keys()), {"id", "nome"})
        for tarefa in projeto["tarefas"]:
            self.assertEqual(set(tarefa.keys()), CHAVES_TAREFA_PROJETO)
        for dia in doc["dias"]:
            self.assertEqual(set(dia.keys()), {"data", "tarefas"})
            for tarefa in dia["tarefas"]:
                self.assertEqual(set(tarefa.keys()), CHAVES_TAREFA_DIA)
        for chave in CHAVES_PROIBIDAS:
            self.assertNotIn(chave, coletar_chaves(doc))
            self.assertNotIn(f'"{chave}"', texto)



class TestStatusNovos(unittest.TestCase):
    def test_carrega_aguardando_e_cancelado(self):
        with tempfile.TemporaryDirectory() as pasta:
            gravar_yaml(pasta, "projeto.yaml", {
                "projeto": "Status novos",
                "fases": [{"id": "F1", "nome": "Fase"}],
                "tarefas": [
                    {"id": "VTX-A", "titulo": "Espera", "fase": "F1", "area": "Qualidade", "prioridade": 1, "status": "aguardando"},
                    {"id": "VTX-B", "titulo": "Fora", "fase": "F1", "area": "Qualidade", "prioridade": 2, "status": "cancelado"},
                    {"id": "VTX-C", "titulo": "Typo", "fase": "F1", "area": "Qualidade", "prioridade": 3, "status": "concluido"},
                ],
            })
            projeto, _dias = carregar(pasta)
        status = {t["id"]: t["status"] for t in projeto["tarefas"]}
        self.assertEqual(status["VTX-A"], "aguardando")
        self.assertEqual(status["VTX-B"], "cancelado")
        self.assertEqual(status["VTX-C"], "a fazer")

    def test_proxima_tarefa_pula_e_progresso_exclui_cancelado(self):
        import subprocess
        with tempfile.TemporaryDirectory() as pasta:
            gravar_yaml(pasta, "projeto.yaml", {
                "projeto": "Fila",
                "fases": [{"id": "F1", "nome": "Fase"}],
                "tarefas": [
                    {"id": "VTX-A", "titulo": "Feita", "fase": "F1", "area": "Qualidade", "prioridade": 1, "status": "concluído"},
                    {"id": "VTX-B", "titulo": "Fora", "fase": "F1", "area": "Qualidade", "prioridade": 2, "status": "cancelado"},
                    {"id": "VTX-C", "titulo": "Espera", "fase": "F1", "area": "Qualidade", "prioridade": 3, "status": "aguardando"},
                    {"id": "VTX-D", "titulo": "Proxima da fila", "fase": "F1", "area": "Qualidade", "prioridade": 4, "status": "a fazer"},
                ],
            })
            script = os.path.join(RAIZ, "scripts", "proxima_tarefa.py")
            saida = subprocess.check_output(["python3", script, pasta], text=True)
        self.assertIn("Progresso: 1/3 (33%)", saida)
        self.assertIn("Próxima: VTX-D", saida)
        self.assertNotIn("VTX-B", saida.split("Próxima:")[-1])
        self.assertNotIn("VTX-C", saida.split("Próxima:")[-1])

    def test_proxima_tarefa_pula_depende_de_nao_concluida(self):
        import subprocess
        with tempfile.TemporaryDirectory() as pasta:
            gravar_yaml(pasta, "projeto.yaml", {
                "projeto": "Fila",
                "fases": [{"id": "F1", "nome": "Fase"}],
                "tarefas": [
                    {"id": "VTX-A", "titulo": "Bloqueada", "fase": "F1", "area": "Qualidade", "prioridade": 1, "status": "a fazer", "depende_de": ["VTX-B"]},
                    {"id": "VTX-B", "titulo": "Pendente", "fase": "F1", "area": "Qualidade", "prioridade": 2, "status": "a fazer"},
                    {"id": "VTX-C", "titulo": "Feita", "fase": "F1", "area": "Qualidade", "prioridade": 3, "status": "concluído"},
                ],
            })
            script = os.path.join(RAIZ, "scripts", "proxima_tarefa.py")
            saida = subprocess.check_output(["python3", script, pasta], text=True)
        self.assertIn("Próxima: VTX-B", saida)
        self.assertNotIn("VTX-A", saida.split("Próxima:")[-1])


if __name__ == "__main__":
    unittest.main()
