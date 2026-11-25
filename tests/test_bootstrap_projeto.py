"""VTX-170: bootstrap gera a estrutura do template e o hello passa lint/testes/build."""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "scripts" / "bootstrap_projeto.sh"

OBRIGATORIOS = [
    "README.md",
    "AGENTS.md",
    ".gitignore",
    ".env.example",
    ".cursor/rules/eficiencia-de-tokens.mdc",
    ".cursor/rules/economia-de-contexto.mdc",
    ".cursor/rules/papeis/planejamento.mdc",
    ".cursor/rules/papeis/execucao.mdc",
    ".github/workflows/ci.yml",
    "docs/produto/PRD.md",
    "docs/arquitetura.md",
    "docs/adr/0000-modelo.md",
    "docs/plano.md",
    "docs/runbook.md",
    "testes/plano.md",
    "src/hello.py",
    "tests/test_hello.py",
]

# Caminhos exigidos em agents/*.md → equivalentes no repositório do cliente.
ARTEFATOS_AGENTES = {
    "docs/arquitetura.md": "docs/arquitetura.md",
    "docs/adr/": "docs/adr/0000-modelo.md",
    "docs/produto/PRD.md": "docs/produto/PRD.md",
    "testes/plano.md": "testes/plano.md",
    "docs/plano.md": "docs/plano.md",
    "docs/runbook.md": "docs/runbook.md",
    ".github/workflows/": ".github/workflows/ci.yml",
}


def _rodar(args, **kwargs):
    return subprocess.run(args, check=False, capture_output=True, text=True, **kwargs)


class TestBootstrapProjeto(unittest.TestCase):
    def test_script_existe_e_e_executavel(self):
        self.assertTrue(SCRIPT.is_file())
        self.assertTrue(os.access(SCRIPT, os.X_OK))

    def test_uso_sem_args_falha(self):
        r = _rodar(["bash", str(SCRIPT)])
        self.assertNotEqual(r.returncode, 0)

    def test_destino_nao_vazio_nao_e_sobrescrito(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "ocupado"
            dest.mkdir()
            (dest / "ja-existia.txt").write_text("não apague\n", encoding="utf-8")
            r = _rodar(["bash", str(SCRIPT), "demo", str(dest)])
            self.assertNotEqual(r.returncode, 0)
            self.assertTrue((dest / "ja-existia.txt").is_file())
            self.assertFalse((dest / "AGENTS.md").exists())

    def test_gera_estrutura_troca_nome_e_hello_verde(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "demo"
            r = _rodar(["bash", str(SCRIPT), "demo", str(dest)], cwd=str(RAIZ))
            self.assertEqual(r.returncode, 0, r.stderr)
            for rel in OBRIGATORIOS:
                self.assertTrue((dest / rel).exists(), f"faltou {rel}")
            for rotulo, rel in ARTEFATOS_AGENTES.items():
                self.assertTrue((dest / rel).exists(), f"artefato de agente ausente ({rotulo} → {rel})")
            readme = (dest / "README.md").read_text(encoding="utf-8")
            self.assertIn("demo", readme)
            self.assertNotIn("__NOME_DO_PROJETO__", readme)
            # Nada do placeholder deve restar.
            restantes = []
            for path in dest.rglob("*"):
                if path.is_file() and ".git" not in path.parts:
                    try:
                        texto = path.read_text(encoding="utf-8")
                    except UnicodeDecodeError:
                        continue
                    if "__NOME_DO_PROJETO__" in texto:
                        restantes.append(str(path.relative_to(dest)))
            self.assertEqual(restantes, [])
            lint = _rodar([sys.executable, "-m", "compileall", "-q", "src", "tests"], cwd=str(dest))
            self.assertEqual(lint.returncode, 0, lint.stderr)
            testes = _rodar([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"], cwd=str(dest))
            self.assertEqual(testes.returncode, 0, testes.stdout + testes.stderr)
            build = _rodar([sys.executable, "-m", "compileall", "-q", "src"], cwd=str(dest))
            self.assertEqual(build.returncode, 0, build.stderr)
            agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("A0", agents)
            self.assertIn("A3", agents)
            self.assertNotIn("github.com/SamAlencar/vtx-core", agents)
            ci = (dest / ".github/workflows/ci.yml").read_text(encoding="utf-8")
            self.assertIn("permissions:", ci)
            self.assertIn("contents: read", ci)
            # bootstrap deve copiar as regras atuais da raiz, não uma cópia velha.
            for nome in ("eficiencia-de-tokens.mdc", "economia-de-contexto.mdc"):
                self.assertEqual(
                    (RAIZ / ".cursor/rules" / nome).read_bytes(),
                    (dest / ".cursor/rules" / nome).read_bytes(),
                    nome,
                )


    def test_regras_de_tokens_sao_iguais_a_fonte(self):
        nomes = [
            "eficiencia-de-tokens.mdc",
            "economia-de-contexto.mdc",
        ]
        for nome in nomes:
            fonte = (RAIZ / ".cursor" / "rules" / nome).read_bytes()
            catalogo = (RAIZ / "knowledge" / "templates" / "cursor" / nome).read_bytes()
            template = (RAIZ / "templates" / "projeto" / ".cursor" / "rules" / nome).read_bytes()
            self.assertEqual(fonte, catalogo, nome)
            self.assertEqual(fonte, template, nome)

    def test_regras_por_papel_do_projeto_gerado_citam_caminhos_existentes(self):
        try:
            from test_agents_md import caminhos_de
        except ModuleNotFoundError:
            from tests.test_agents_md import caminhos_de

        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "demo"
            r = _rodar(["bash", str(SCRIPT), "demo", str(dest)], cwd=str(RAIZ))
            self.assertEqual(r.returncode, 0, r.stderr)
            raiz = dest.resolve()
            papeis = sorted((dest / ".cursor/rules/papeis").glob("*.mdc"))
            self.assertTrue(papeis, "faltaram regras por papel no projeto gerado")
            falhas = []
            for path in papeis:
                texto = path.read_text(encoding="utf-8")
                # Não podem sobrar caminhos que só existem no vtx-core.
                for trecho in (
                    "templates/projeto/",
                    "knowledge/processos/",
                    "knowledge/INDEX.md",
                    "agents/",
                    "backlog/",
                ):
                    if trecho in texto:
                        falhas.append(
                            f"{path.relative_to(dest)}: cita caminho do vtx-core ({trecho})"
                        )
                for url, alvo in caminhos_de(path, raiz=raiz):
                    try:
                        alvo.relative_to(raiz)
                    except ValueError:
                        falhas.append(f"{path.relative_to(dest)}: {url} sai do projeto")
                        continue
                    if not alvo.exists():
                        falhas.append(
                            f"{path.relative_to(dest)}: caminho ausente {url}"
                        )
            self.assertEqual(falhas, [])


if __name__ == "__main__":
    unittest.main()
