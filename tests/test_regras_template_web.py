"""VTX-210: regras do template web com globs, caminhos e exemplos sincronizados."""
from __future__ import annotations

import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    from test_agents_md import caminhos_de
except ModuleNotFoundError:
    from tests.test_agents_md import caminhos_de

RAIZ = Path(__file__).resolve().parents[1]
TEMPLATE = RAIZ / "templates" / "web-next"
REGRAS = ("stack.mdc", "api.mdc", "agentes.mdc")
CERCAS = re.compile(r"^```(?:ts|tsx|typescript)\s*\n([\s\S]*?)```", re.M)
SCRIPT = RAIZ / "scripts" / "bootstrap_projeto.sh"


def _extrair(texto: str) -> str:
    m = CERCAS.search(texto)
    if not m:
        raise AssertionError("nenhum bloco ts")
    return m.group(1).rstrip() + "\n"


def _rodar(args, **kwargs):
    return subprocess.run(args, check=False, capture_output=True, text=True, **kwargs)


class TestRegrasTemplateWeb(unittest.TestCase):
    def test_tres_regras_existem_com_globs_nao_vazios(self):
        for nome in REGRAS:
            path = TEMPLATE / ".cursor" / "rules" / nome
            self.assertTrue(path.is_file(), nome)
            texto = path.read_text(encoding="utf-8")
            self.assertIn("alwaysApply: false", texto)
            self.assertNotIn("alwaysApply: true", texto)
            linhas_glob = [ln for ln in texto.splitlines() if ln.startswith("globs:")]
            self.assertEqual(len(linhas_glob), 1, nome)
            valor = linhas_glob[0].split(":", 1)[1].strip()
            self.assertTrue(valor, f"glob vazio em {nome}")
            self.assertNotIn("{", linhas_glob[0], nome)
            self.assertIsNotNone(CERCAS.search(texto), f"sem bloco de código em {nome}")

    def test_exemplos_extraidos_batem_com_as_cercas(self):
        for nome in REGRAS:
            mdc = (TEMPLATE / ".cursor" / "rules" / nome).read_text(encoding="utf-8")
            esperado = _extrair(mdc)
            gerado = TEMPLATE / "tests" / "regras" / nome.replace(".mdc", ".exemplo.ts")
            self.assertTrue(gerado.is_file(), gerado.name)
            self.assertEqual(gerado.read_text(encoding="utf-8"), esperado, gerado.name)

    def test_ponteiro_do_vtx_core_cita_as_regras(self):
        path = RAIZ / ".cursor" / "rules" / "template-web-engenharia.mdc"
        self.assertTrue(path.is_file())
        texto = path.read_text(encoding="utf-8")
        self.assertIn("alwaysApply: false", texto)
        self.assertIn("globs:", texto)
        for trecho in (
            "templates/web-next/.cursor/rules/stack.mdc",
            "templates/web-next/.cursor/rules/api.mdc",
            "templates/web-next/.cursor/rules/agentes.mdc",
            "templates/web-next/DESIGN.md",
            "templates/web-next/AGENTS.md",
        ):
            self.assertIn(trecho, texto)
        falhas = []
        for url, alvo in caminhos_de(path, raiz=RAIZ):
            if not alvo.exists():
                falhas.append(f"ponteiro: caminho ausente {url}")
        self.assertEqual(falhas, [])

    def test_projeto_web_gerado_tem_regras_design_e_caminhos(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "demo-web"
            r = _rodar(["bash", str(SCRIPT), "--tipo", "web", "demo-web", str(dest)], cwd=str(RAIZ))
            self.assertEqual(r.returncode, 0, r.stderr)
            for rel in (
                ".cursor/rules/stack.mdc",
                ".cursor/rules/api.mdc",
                ".cursor/rules/agentes.mdc",
                "DESIGN.md",
                "AGENTS.md",
                "lib/http/problema.ts",
                "src/dominio/exemplo/index.ts",
                "src/agentes/prompts/exemplo.ts",
                "src/agentes/tools/exemplo.ts",
                "src/agentes/harness/executar.ts",
                "app/api/exemplo/route.ts",
                "tests/regras/stack.exemplo.ts",
                "tests/regras/api.exemplo.ts",
                "tests/regras/agentes.exemplo.ts",
            ):
                self.assertTrue((dest / rel).is_file(), rel)
            agents = (dest / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("DESIGN.md", agents)
            self.assertIn(".cursor/rules/stack.mdc", agents)
            design = (dest / "DESIGN.md").read_text(encoding="utf-8")
            self.assertIn("demo-web", design)
            self.assertNotIn("__NOME_DO_PROJETO__", design)
            # o ponteiro do vtx-core não vai para o cliente
            self.assertFalse((dest / ".cursor/rules/template-web-engenharia.mdc").exists())
            falhas = []
            raiz = dest.resolve()
            for nome in (*REGRAS,):
                path = dest / ".cursor" / "rules" / nome
                for url, alvo in caminhos_de(path, raiz=raiz):
                    try:
                        alvo.relative_to(raiz)
                    except ValueError:
                        falhas.append(f"{nome}: {url} sai do projeto")
                        continue
                    if not alvo.exists():
                        falhas.append(f"{nome}: caminho ausente {url}")
            self.assertEqual(falhas, [])


if __name__ == "__main__":
    unittest.main()
