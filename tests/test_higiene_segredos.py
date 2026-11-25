"""VTX-173: .gitignore, .env.example e pre-commit com gitleaks na raiz."""
from __future__ import annotations

import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]


class TestHigieneSegredos(unittest.TestCase):
    def test_gitignore_cobre_segredos_e_artefatos(self):
        texto = (RAIZ / ".gitignore").read_text(encoding="utf-8")
        for trecho in (".env", ".env.*", "!.env.example", "node_modules/", "dist/", "*.db", "*.sqlite", ".venv/"):
            self.assertIn(trecho, texto)

    def test_env_example_existe_e_sem_segredo(self):
        path = RAIZ / ".env.example"
        self.assertTrue(path.is_file())
        texto = path.read_text(encoding="utf-8")
        self.assertIn(".env", texto)
        for suspeito in ("sk-", "ghp_", "AKIA", "-----BEGIN"):
            self.assertNotIn(suspeito, texto)

    def test_pre_commit_usa_gitleaks_alinhado_ao_ci(self):
        pre = (RAIZ / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        self.assertIn("gitleaks", pre)
        self.assertIn("v8.30.1", pre)
        ci = (RAIZ / ".github/workflows/testes.yml").read_text(encoding="utf-8")
        self.assertIn('GITLEAKS_VERSION: "8.30.1"', ci)
        readme = (RAIZ / "README.md").read_text(encoding="utf-8")
        self.assertIn("pre-commit install", readme)
        self.assertIn("gitleaks", readme)


if __name__ == "__main__":
    unittest.main()
