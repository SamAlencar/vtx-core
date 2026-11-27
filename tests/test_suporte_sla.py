"""VTX-199: pacote técnico de manutenção, SLA e suporte."""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "scripts"))
from verificar_links import verificar

DOC = RAIZ / "knowledge/operacao/suporte-e-sla.md"
RUNBOOK = RAIZ / "templates/web-next/docs/runbook.md"
MODELO = RAIZ / "templates/web-next/docs/postmortems/0000-modelo.md"
MANUT = RAIZ / "knowledge/processos/fluxos/manutencao-evolucao.md"
DEVOPS = RAIZ / "knowledge/operacao/devops-sre.md"
INDEX = RAIZ / "knowledge/INDEX.md"
BOOTSTRAP = RAIZ / "scripts/bootstrap_projeto.sh"


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
            "compromisso contratual",
            "meta interna",
        ):
            self.assertIn(trecho, lower)
        self.assertIn("docs/postmortems/AAAA-MM-DD-titulo.md", texto)
        self.assertNotIn("YYYY-MM-DD-<slug>", texto)
        self.assertNotIn("projects/<cliente>/docs/postmortems/", texto)
        self.assertIn("dependência externa", lower)
        self.assertRegex(lower, r"preço|venda")

    def test_alinha_devops_aviso_e_nome_do_arquivo(self):
        suporte = DOC.read_text(encoding="utf-8")
        devops = DEVOPS.read_text(encoding="utf-8")
        runbook = RUNBOOK.read_text(encoding="utf-8")
        for texto in (suporte, devops, runbook):
            self.assertIn("AAAA-MM-DD-titulo.md", texto)
            self.assertIn("no mesmo dia", texto)
        self.assertIn("compromisso contratual", suporte.lower())
        self.assertIn("meta interna de mitigação", devops.lower())
        self.assertIn("compromisso contratual", runbook.lower())
        self.assertIn("meta interna", runbook.lower())

    def test_ponteiros_runbook_autossuficiente_e_modelo(self):
        runbook = RUNBOOK.read_text(encoding="utf-8")
        manut = MANUT.read_text(encoding="utf-8")
        devops = DEVOPS.read_text(encoding="utf-8")
        self.assertTrue(MODELO.is_file())
        self.assertIn("AAAA-MM-DD-titulo.md", MODELO.read_text(encoding="utf-8"))
        self.assertIn("postmortems/0000-modelo.md", runbook)
        self.assertNotIn("](../../../knowledge/", runbook)
        self.assertNotIn("](../../knowledge/", runbook)
        # Citação opcional em texto, sem link relativo para fora do repo do cliente.
        self.assertIn("knowledge/operacao/suporte-e-sla.md", runbook)
        self.assertIn("UptimeRobot", runbook)
        self.assertIn("/api/health", runbook)
        self.assertIn("ainda não existe", runbook)
        self.assertIn("suporte-e-sla.md", manut)
        self.assertIn("SLA técnico", manut)
        self.assertIn("suporte-e-sla.md", devops)

    def test_projeto_web_gerado_tem_links_relativos_validos(self):
        """Espelha o job web-gerado: bootstrap --tipo web e confere os docs gerados."""
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "demo-web"
            r = subprocess.run(
                ["bash", str(BOOTSTRAP), "--tipo", "web", "demo-web", str(dest)],
                cwd=str(RAIZ),
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertTrue((dest / "docs/runbook.md").is_file())
            self.assertTrue((dest / "docs/postmortems/0000-modelo.md").is_file())
            gerado = (dest / "docs/runbook.md").read_text(encoding="utf-8")
            self.assertNotIn("__NOME_DO_PROJETO__", gerado)
            self.assertNotIn("](../../../knowledge/", gerado)
            erros = verificar(str(dest))
            docs = [e for e in erros if "/docs/" in e.replace("\\", "/") or e.startswith("docs/")]
            self.assertEqual(docs, [], "\n".join(docs))
            # O verificador no projeto inteiro também precisa passar:
            # links quebrados em qualquer .md copiado quebram o cliente.
            self.assertEqual(erros, [], "\n".join(erros))


if __name__ == "__main__":
    unittest.main()
