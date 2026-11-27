"""VTX-179: telemetria por execução de agente."""
import json
import subprocess
import tempfile
import unittest
from datetime import UTC, datetime
from pathlib import Path

from agente.telemetria import (
    OrcamentoExcedido,
    Telemetria,
    custo_por_cliente_dia,
    custo_usd,
    ler,
    ler_detalhado,
    redigir,
)

DIA = datetime(2026, 11, 27, 12, tzinfo=UTC)
RAIZ = Path(__file__).resolve().parents[1]


class TestTelemetria(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.caminho = Path(self.tmp.name) / "exec.jsonl"
        self.t = Telemetria(self.caminho, orcamento_dia={"acme": 0.01}, agora=lambda: DIA)

    def tearDown(self):
        self.tmp.cleanup()

    def test_uma_linha_json_com_campos(self):
        with self.t.execucao("acme", "orquestrador", "modelo-x", trace_id="t1") as ex:
            ex.somar(1000, 200, custo_usd(1000, 200, 3.0, 15.0))
        linhas = self.caminho.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(linhas), 1)
        x = json.loads(linhas[0])
        for campo in ("run_id", "trace_id", "cliente", "tokens_entrada", "tokens_saida",
                      "custo_usd", "duracao_ms", "status", "ts"):
            self.assertIn(campo, x)
        self.assertEqual((x["trace_id"], x["custo_usd"], x["status"]), ("t1", 0.006, "ok"))

    def test_redacao_de_pii(self):
        texto = (
            "cpf 123.456.789-09, mail ana@ex.com.br, cnpj 12.345.678/0001-90 e 12345678000190, "
            "tel (11) 98765-4321, sk-abcdefghijklmnop1234, Bearer abc.def.ghi123"
        )
        r = redigir({"msg": texto, "lista": ["ghp_" + "a" * 36]})
        dumped = json.dumps(r)
        for vazado in ("123.456.789-09", "ana@ex.com.br", "12.345.678/0001-90",
                       "12345678000190", "(11) 98765-4321", "sk-abcdef", "abc.def.ghi123", "ghp_"):
            self.assertNotIn(vazado, dumped)
        self.assertIn("[CPF]", r["msg"])
        self.assertIn("[EMAIL]", r["msg"])
        self.assertIn("[CNPJ]", r["msg"])
        self.assertIn("[TELEFONE]", r["msg"])
        # 11 dígitos sem máscara (celular ou CPF) ficam de fora.
        self.assertEqual(redigir("celular 11987654321"), "celular 11987654321")

    def test_erro_grava_linha_redigida_e_repropaga(self):
        with self.assertRaises(ValueError), self.t.execucao("acme", "dev"):
            raise ValueError("falhou para ana@ex.com")
        x = ler(self.caminho)[0]
        self.assertEqual(x["status"], "erro")
        self.assertIn("[EMAIL]", x["erro"])

    def test_baseexception_grava_erro_e_repropaga(self):
        with self.assertRaises(KeyboardInterrupt), self.t.execucao("acme", "dev"):
            raise KeyboardInterrupt()
        x = ler(self.caminho)[0]
        self.assertEqual(x["status"], "erro")
        self.assertIn("KeyboardInterrupt", x["erro"])

    def test_cliente_email_nao_e_redigido_e_orcamento_barra(self):
        cliente = "ana@ex.com"
        t = Telemetria(self.caminho, orcamento_dia={cliente: 0.01}, agora=lambda: DIA)
        with t.execucao(cliente, "dev") as ex:
            ex.somar(0, 0, 0.5)
        x = ler(self.caminho)[0]
        self.assertEqual(x["cliente"], cliente)
        rodou = []
        with self.assertRaises(OrcamentoExcedido), t.execucao(cliente, "dev"):
            rodou.append(1)
        self.assertEqual(rodou, [])

    def test_linha_corrompida_nao_bloqueia_e_e_contada(self):
        self.caminho.write_text(
            '{"cliente": "acme", "ts": "2026-11-27T10:00:00+00:00", "custo_usd": 0.001}\n'
            "{isto nao e json\n",
            encoding="utf-8",
        )
        linhas, invalidas = ler_detalhado(self.caminho)
        self.assertEqual(len(linhas), 1)
        self.assertEqual(invalidas, 1)
        with self.t.execucao("acme", "dev"):
            pass
        self.assertEqual(len(ler(self.caminho)), 2)

    def test_soma_por_cliente_e_dia(self):
        linhas = [
            {"cliente": "acme", "ts": "2026-11-27T10:00:00+00:00", "custo_usd": 0.5},
            {"cliente": "acme", "ts": "2026-11-27T11:00:00+00:00", "custo_usd": 0.25},
            {"cliente": "acme", "ts": "2026-11-28T09:00:00+00:00", "custo_usd": 1.0},
            {"cliente": "beta", "ts": "2026-11-27T09:00:00+00:00", "custo_usd": 2.0},
        ]
        self.assertEqual(custo_por_cliente_dia(linhas), {
            ("acme", "2026-11-27"): 0.75, ("acme", "2026-11-28"): 1.0, ("beta", "2026-11-27"): 2.0})

    def test_orcamento_interrompe_antes_de_executar(self):
        with self.t.execucao("acme", "dev") as ex:
            ex.somar(0, 0, 0.02)
        rodou = []
        with self.assertRaises(OrcamentoExcedido), self.t.execucao("acme", "dev"):
            rodou.append(1)
        self.assertEqual(rodou, [])
        self.assertEqual(len(ler(self.caminho)), 1)
        with self.t.execucao("beta", "dev"):
            pass
        self.assertEqual(len(ler(self.caminho)), 2)

    def test_logs_de_agente_estao_no_gitignore(self):
        r = subprocess.run(
            ["git", "-C", str(RAIZ), "check-ignore", "-q", "logs/agentes.jsonl"],
            check=False,
        )
        self.assertEqual(r.returncode, 0)


if __name__ == "__main__":
    unittest.main()
