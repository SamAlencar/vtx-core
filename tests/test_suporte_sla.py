"""VTX-199: pacote técnico de manutenção, SLA e suporte."""
from __future__ import annotations

import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
DOC = RAIZ / "knowledge/operacao/suporte-e-sla.md"
RUNBOOK = RAIZ / "templates/web-next/docs/runbook.md"
MANUT = RAIZ / "knowledge/processos/fluxos/manutencao-evolucao.md"
DEVOPS = RAIZ / "knowledge/operacao/devops-sre.md"
INDEX = RAIZ / "knowledge/INDEX.md"


class TestSuporteSla(unittest.TestCase):
    def test_documento_e_indice(self):
        self.assertTrue(DOC.is_file())
        index = INDEX.read_text(encoding="utf-8")
        self.assertIn("operacao/suporte-e-sla.md", index)
        self.assertRegex(
            index,
            r"\| 63 \| \[Pacote técnico de manutenção, SLA e suporte\]\(operacao/suporte-e-sla.md\)",
        )

    def test_aceite_dois_niveis_canal_monitor_postmortem(self):
        texto = DOC.read_text(encoding="utf-8")
        lower = texto.lower()
        for trecho in (
            "essencial",
            "evolução",
            "4 h",
            "12 h",
            "4 h úteis",
            "1 dia útil",
            "3 dias úteis",
            "e-mail",
            "formulário",
            "triagem",
            "uptimerobot",
            "better stack",
            "docs/postmortems/",
            "repositório do cliente",
        ):
            self.assertIn(trecho, lower)
        self.assertNotIn("projects/<cliente>/docs/postmortems/", texto)
        # Preço e venda ficam fora do aceite.
        self.assertIn("dependência externa", lower)
        self.assertRegex(lower, r"preço|venda")

    def test_ponteiros_e_runbook(self):
        runbook = RUNBOOK.read_text(encoding="utf-8")
        manut = MANUT.read_text(encoding="utf-8")
        devops = DEVOPS.read_text(encoding="utf-8")
        self.assertIn("suporte-e-sla.md", runbook)
        self.assertIn("UptimeRobot", runbook)
        self.assertIn("docs/postmortems/", runbook)
        self.assertIn("/api/health", runbook)
        self.assertIn("ainda não existe", runbook)
        self.assertIn("suporte-e-sla.md", manut)
        self.assertIn("SLA técnico", manut)
        self.assertIn("suporte-e-sla.md", devops)


if __name__ == "__main__":
    unittest.main()
