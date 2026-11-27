"""Guarda de DADOS dos scripts de Postgres temporário: só valida, não apaga."""

from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
LIB = RAIZ / "templates" / "web-next" / "scripts" / "lib" / "guarda_dados_pg.sh"

# Caminhos reais do box compartilhado: a suíte só chama validar_dados, nunca
# remover_dados, e não cria nem escreve nesses diretórios.
OPENFINANCE = Path("/workspace/openfinance")
EVOLUTION = Path("/home/box/evolution-pgdata")


def _validar(dados: str, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    script = r"""
set -euo pipefail
NOME=teste-guarda
# shellcheck source=/dev/null
source "$LIB_GUARDA"
validar_dados "$DADOS_TESTE"
printf '%s\n' "$DADOS"
"""
    ambiente = os.environ.copy()
    if env:
        ambiente.update(env)
    ambiente["LIB_GUARDA"] = str(LIB)
    ambiente["DADOS_TESTE"] = dados
    return subprocess.run(
        ["bash", "-c", script],
        check=False,
        capture_output=True,
        text=True,
        env=ambiente,
    )


class TestGuardaDadosPg(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not LIB.is_file():
            raise AssertionError(f"lib não encontrada: {LIB}")
        cls._openfinance_antes = (
            OPENFINANCE.exists(),
            OPENFINANCE.stat().st_mtime_ns if OPENFINANCE.exists() else None,
        )
        cls._evolution_antes = (
            EVOLUTION.exists(),
            EVOLUTION.stat().st_mtime_ns if EVOLUTION.exists() else None,
        )

    def tearDown(self) -> None:
        self._afirmar_intocado(OPENFINANCE, self._openfinance_antes)
        self._afirmar_intocado(EVOLUTION, self._evolution_antes)

    def _afirmar_intocado(self, caminho: Path, antes: tuple[bool, int | None]) -> None:
        existia, mtime = antes
        if existia:
            self.assertTrue(caminho.exists(), f"{caminho} foi apagado")
            self.assertEqual(caminho.stat().st_mtime_ns, mtime, f"{caminho} foi modificado")
        else:
            self.assertFalse(caminho.exists(), f"{caminho} foi criado")

    def _recusa(self, dados: str, **kwargs: str) -> None:
        r = _validar(dados, env=kwargs or None)
        self.assertEqual(r.returncode, 2, f"devia recusar {dados!r}: {r.stdout}{r.stderr}")
        self.assertIn("recuso", r.stderr)

    def _aceita(self, dados: str, esperado: str, **kwargs: str) -> None:
        r = _validar(dados, env=kwargs or None)
        self.assertEqual(r.returncode, 0, f"devia aceitar {dados!r}: {r.stderr}")
        self.assertEqual(r.stdout.strip(), esperado)

    def test_recusa_openfinance_workspace_raiz_e_vazio(self) -> None:
        self._recusa("/workspace/openfinance")
        self._recusa("/workspace")
        self._recusa("/workspace/")
        self._recusa("/")
        self._recusa("")

    def test_recusa_travessia(self) -> None:
        self._recusa("/workspace/pg-acoes-x/../openfinance")
        self._recusa("/workspace/foo/../..")
        self._recusa("/workspace/../etc")
        self._recusa("/workspace/pg-acoes-x/../../..")

    def test_recusa_symlink_para_fora(self) -> None:
        with tempfile.TemporaryDirectory(prefix="guarda-dados-", dir="/tmp") as tmp:
            link = Path(tmp) / "pg-acoes-link"
            # Só cria o symlink; não toca no destino.
            link.symlink_to("/workspace/openfinance")
            self.assertTrue(link.is_symlink())
            self._recusa(str(link))
            ev = Path(tmp) / "pg-acoes-evo"
            ev.symlink_to("/home/box/evolution-pgdata")
            self._recusa(str(ev))
            self.assertTrue(link.is_symlink())
            self.assertTrue(ev.is_symlink())

    def test_recusa_evolution_e_tmp_generico(self) -> None:
        self._recusa("/home/box/evolution-pgdata")
        self._recusa("/tmp")
        self._recusa("/etc")
        self._recusa("/tmp/nao-e-pg-acoes")

    def test_aceita_workspace_pg_acoes(self) -> None:
        self._aceita("/workspace/pg-acoes-x", "/workspace/pg-acoes-x")
        self._aceita("/workspace/pg-acoes-rls-tmp", "/workspace/pg-acoes-rls-tmp")
        self._aceita(
            "/workspace/pg-acoes-rpc-nulo-tmp",
            "/workspace/pg-acoes-rpc-nulo-tmp",
        )

    def test_aceita_mktemp(self) -> None:
        with tempfile.TemporaryDirectory(prefix="pg-acoes-", dir="/tmp") as d:
            self._aceita(d, str(Path(d).resolve()))
            # o diretório de teste continua lá: a guarda não apaga
            self.assertTrue(Path(d).is_dir())

    def test_scripts_fazem_source_da_lib(self) -> None:
        pasta = RAIZ / "templates" / "web-next" / "scripts"
        for nome in ("teste-rls-acoes.sh", "teste-rpc-acoes-composto-nulo.sh"):
            texto = (pasta / nome).read_text(encoding="utf-8")
            self.assertIn('source "$LIB_GUARDA"', texto)
            self.assertIn("lib/guarda_dados_pg.sh", texto)
            self.assertNotIn("if [[ \"$canon\" == /workspace/* ]]; then", texto)


if __name__ == "__main__":
    unittest.main()
