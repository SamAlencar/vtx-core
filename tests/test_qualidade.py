"""Testes dos portões de qualidade: backlog, INDEX e links relativos."""
import os
import tempfile
import unittest
from pathlib import Path

import yaml

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
import sys

sys.path.insert(0, os.path.join(RAIZ, "scripts"))
from validar_backlog import validar
from verificar_links import verificar


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

    def test_testes_yml_permissions_no_topo(self) -> None:
        caminho = Path(RAIZ, ".github", "workflows", "testes.yml")
        wf = yaml.safe_load(caminho.read_text(encoding="utf-8"))
        self.assertEqual(wf["permissions"], {"contents": "read"})


class TestPipelinePainelAposentado(unittest.TestCase):
    def test_workflow_e_citacoes_ativas_ausentes(self):
        self.assertFalse(
            Path(RAIZ, ".github/workflows/sincronizar-painel.yml").exists()
        )
        readme = Path(RAIZ, "README.md").read_text(encoding="utf-8")
        self.assertIn("https://samalencar.github.io/painel-central/", readme)
        self.assertNotIn("Sincronização automática do painel (ativa)", readme)
        inicio = readme.find("## Arquitetura")
        self.assertGreaterEqual(inicio, 0)
        fim = readme.find('\n## ', inicio + 1)
        secao = readme[inicio:fim if fim != -1 else None]
        # Só a tabela de componentes; a sentença de aposentadoria pode citar o nome antigo.
        idx = secao.find("| Componente |")
        self.assertGreaterEqual(idx, 0, secao[:200])
        fim_tabela = secao.find('\n\n', idx)
        tabela = secao[idx:fim_tabela if fim_tabela != -1 else None]
        self.assertNotIn("vtx_painel", tabela)
        pasta = Path(RAIZ, ".github/workflows")
        self.assertTrue(pasta.is_dir())
        for caminho in pasta.iterdir():
            if caminho.is_file():
                texto = caminho.read_text(encoding="utf-8")
                self.assertNotIn("PANEL_TOKEN", texto, caminho.name)
                self.assertNotIn("vtx_painel", texto, caminho.name)
                self.assertNotIn("sincronizar-painel", texto, caminho.name)


if __name__ == "__main__":
    unittest.main()
