"""Testes dos portões de qualidade: backlog, INDEX e links relativos."""
import os
import tempfile
import unittest
from pathlib import Path

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys
sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from validar_backlog import validar  # noqa: E402
from verificar_links import verificar  # noqa: E402


def _escrever(raiz: Path, rel: str, texto: str):
    caminho = raiz / rel
    caminho.parent.mkdir(parents=True, exist_ok=True)
    caminho.write_text(texto, encoding="utf-8")


def _backlog_minimo(pasta: Path, tarefas):
    _escrever(pasta, "backlog/projeto.yaml", yaml.safe_dump({
        "projeto": "Teste",
        "fases": [{"id": "F0", "nome": "Fundação"}, {"id": "F8", "nome": "Qualidade"}],
        "tarefas": tarefas,
    }, allow_unicode=True, sort_keys=False))
    _escrever(pasta, "knowledge/INDEX.md", "# Índice\n")


class TestValidarBacklog(unittest.TestCase):
    def test_f0_sem_entregavel_passa(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _backlog_minimo(pasta, [{
                "id": "VTX-001", "titulo": "Fundação", "fase": "F0",
                "area": "Organização", "prioridade": 1, "status": "concluído",
            }])
            self.assertEqual(validar(str(pasta), str(pasta / "backlog")), [])

    def test_concluida_sem_arquivo_falha(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _backlog_minimo(pasta, [{
                "id": "VTX-100", "titulo": "Doc", "fase": "F8",
                "area": "Qualidade", "prioridade": 1, "status": "concluído",
                "entregavel": "knowledge/sumido.md",
            }])
            erros = validar(str(pasta), str(pasta / "backlog"))
            self.assertTrue(any("entregável ausente" in e for e in erros))

    def test_knowledge_fora_do_index_falha(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _backlog_minimo(pasta, [{
                "id": "VTX-001", "titulo": "Fundação", "fase": "F0",
                "area": "Organização", "prioridade": 1, "status": "a fazer",
            }])
            _escrever(pasta, "knowledge/solto.md", "# Solto\n")
            erros = validar(str(pasta), str(pasta / "backlog"))
            self.assertTrue(any("solto.md não aparece no INDEX.md" in e for e in erros))


class TestVerificarLinks(unittest.TestCase):
    def test_link_relativo_quebrado_falha(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _escrever(pasta, "docs/a.md", "[x](falta.md)\n")
            erros = verificar(str(pasta))
            self.assertTrue(any("falta.md" in e for e in erros))

    def test_link_ok_e_externo_passam(self):
        with tempfile.TemporaryDirectory() as tmp:
            pasta = Path(tmp)
            _escrever(pasta, "docs/alvo.md", "ok\n")
            _escrever(pasta, "docs/a.md", "[x](alvo.md) [y](https://example.com) [z](#secao)\n")
            self.assertEqual(verificar(str(pasta)), [])


class TestPortaoNoRepoReal(unittest.TestCase):
    def test_backlog_e_index_atuais(self):
        self.assertEqual(validar(RAIZ, os.path.join(RAIZ, "backlog")), [])

    def test_links_relativos_atuais(self):
        self.assertEqual(verificar(RAIZ), [])


if __name__ == "__main__":
    unittest.main()
