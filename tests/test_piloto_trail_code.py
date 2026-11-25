"""VTX-135: piloto do Trail-code documentado, com sandbox isolado e sem init/--deep."""
from __future__ import annotations

import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DOC = RAIZ / "knowledge/ferramentas/piloto-trail-code.md"
SANDBOX = RAIZ / "projects/sandbox-trail-code"
SCRIPT = SANDBOX / "scripts/rodar-piloto.sh"
GITIGNORE = SANDBOX / ".gitignore"
PACKAGE = SANDBOX / "package.json"


class TestPilotoTrailCode(unittest.TestCase):
    def test_documentos_e_sandbox_existem(self):
        for path in (DOC, SCRIPT, GITIGNORE, PACKAGE, SANDBOX / "README.md"):
            self.assertTrue(path.is_file(), path.relative_to(RAIZ))
        self.assertTrue((SANDBOX / "exemplos/skeleton-medida.txt").is_file())
        self.assertTrue((SANDBOX / "exemplos/tempo-build.txt").is_file())
        self.assertTrue((SANDBOX / "exemplos/ask-proxima-tarefa-amostra.txt").is_file())
        self.assertTrue((SANDBOX / "exemplos/build-resumo.txt").is_file())
        self.assertTrue((SANDBOX / "package-lock.json").is_file())

    def test_pin_telemetria_e_comandos_proibidos(self):
        script = SCRIPT.read_text(encoding="utf-8")
        package = PACKAGE.read_text(encoding="utf-8")
        self.assertIn("DO_NOT_TRACK=1", script)
        self.assertIn("telemetry disable", script)
        self.assertIn("@nanonets/graft", package)
        self.assertIn("0.23.1", package)
        self.assertIn("npm ci", script)
        self.assertIn("--ignore-scripts", script)
        self.assertIn('"$GRAFT" stats', script)
        self.assertNotIn('"$GRAFT" status', script)
        # Isola HOME no sandbox, não no usuário do agente.
        self.assertIn('.home', script)
        # Não invoca init nem --deep (podem aparecer só como proibição).
        invocacoes_init = re.findall(r'^\s*"?\$\{?GRAFT\}?"?\s+init\b', script, re.M)
        invocacoes_deep = re.findall(r'^\s*"?\$\{?GRAFT\}?"?\s+build\s+--deep\b', script, re.M)
        self.assertEqual(invocacoes_init, [])
        self.assertEqual(invocacoes_deep, [])
        self.assertNotRegex(script, r"(?m)^\s*npm\s+install\s+-g\b")

    def test_gitignore_esconde_artefatos_gerados(self):
        texto = GITIGNORE.read_text(encoding="utf-8")
        for trecho in ("node_modules", ".home", ".npm-cache", ".trail", "tmp-repo", "saida-bruta"):
            self.assertIn(trecho, texto)
        self.assertNotIn("package-lock.json", texto)

    def test_relato_registra_decisao_e_medidas(self):
        texto = DOC.read_text(encoding="utf-8")
        lower = texto.lower()
        for trecho in (
            "adotado com restrições",
            "0.23.1",
            "DO_NOT_TRACK",
            "build --deep",
            "init",
            "scripts/backlog_lib.py",
            "27%",
        ):
            self.assertIn(trecho.lower(), lower)
        self.assertIn("mcp", lower)
        self.assertIn("entra no vtx-core nesta etapa", lower)
        resumo = (SANDBOX / "exemplos/build-resumo.txt").read_text(encoding="utf-8")
        self.assertRegex(resumo, r"commit [0-9a-f]{7,40}")
        self.assertRegex(resumo, r"\d+ nodes")
        self.assertRegex(resumo, r"\d+ edges")
        self.assertRegex(resumo, r"parsed: \d+ of \d+ files")

    def test_index_aponta_para_o_piloto(self):
        index = (RAIZ / "knowledge/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("ferramentas/piloto-trail-code.md", index)


if __name__ == "__main__":
    unittest.main()
