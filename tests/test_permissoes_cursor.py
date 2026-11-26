"""VTX-224: deny rules do Cursor (.cursor/cli.json) e segredos fora do contexto (.cursorignore)."""
from __future__ import annotations

import fnmatch
import json
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
CLI = RAIZ / ".cursor" / "cli.json"
IGNORES = (RAIZ / ".cursorignore", RAIZ / "knowledge" / "templates" / "cursor" / ".cursorignore")

DENY_OBRIGATORIOS = (
    "Read(**/.env)",
    "Read(**/.env.local)",
    "Read(**/*.pem)",
    "Read(**/*.key)",
    "Read(~/.ssh/**)",
    "Write(**/.env)",
    "Write(**/*.key)",
    "Shell(sudo)",
    "Shell(rm:-rf *)",
    "Shell(git:push --force)",
    "Shell(git:push * --force *)",
    "Shell(git:push -f *)",
    "Shell(git:push * main)",
    "Shell(git:push * --delete *)",
    "Shell(git:reset --hard*)",
    "Shell(gh:repo delete*)",
)


def _deny(texto: str) -> list[str]:
    return json.loads(texto)["permissions"]["deny"]


def _ativos(path: Path) -> list[str]:
    linhas = path.read_text(encoding="utf-8").splitlines()
    return [l.strip() for l in linhas if l.strip() and not l.strip().startswith("#")]


def _ignorado(padroes: list[str], nome: str) -> bool:
    """Semântica mínima de .gitignore para nomes de arquivo: o último padrão que casa decide."""
    resultado = False
    for p in padroes:
        negado = p.startswith("!")
        alvo = p[1:] if negado else p
        if fnmatch.fnmatch(nome, alvo):
            resultado = not negado
    return resultado


class TestPermissoesCursor(unittest.TestCase):
    def test_cli_json_valido_e_so_com_permissoes(self):
        dados = json.loads(CLI.read_text(encoding="utf-8"))
        self.assertEqual(set(dados), {"permissions"})
        self.assertEqual(set(dados["permissions"]), {"allow", "deny"})
        self.assertEqual(dados["permissions"]["allow"], [])

    def test_deny_obrigatorios(self):
        deny = _deny(CLI.read_text(encoding="utf-8"))
        for regra in DENY_OBRIGATORIOS:
            self.assertIn(regra, deny)
        self.assertEqual(len(deny), len(set(deny)))

    def test_tokens_com_tipo_conhecido(self):
        for regra in _deny(CLI.read_text(encoding="utf-8")):
            tipo = regra.split("(", 1)[0]
            self.assertIn(tipo, {"Shell", "Read", "Write", "WebFetch", "Mcp"}, regra)
            self.assertTrue(regra.endswith(")"), regra)

    def test_force_with_lease_em_branch_propria_nao_bloqueado(self):
        # Rebase de branch de PR usa --force-with-lease; o bloqueio é para --force puro.
        comando = "push --force-with-lease origin vtx-123"
        padroes = [r[len("Shell(git:"):-1] for r in _deny(CLI.read_text(encoding="utf-8")) if r.startswith("Shell(git:push")]
        self.assertFalse(any(fnmatch.fnmatchcase(comando, p) for p in padroes))
        self.assertTrue(any(fnmatch.fnmatchcase("push --force origin main", p) for p in padroes))

    def test_cursorignore_esconde_segredos_e_mostra_exemplo(self):
        for path in IGNORES:
            padroes = _ativos(path)
            for nome in (".env", ".env.local", ".env.production", "servidor.pem", "privada.key", "id_ed25519", ".npmrc"):
                self.assertTrue(_ignorado(padroes, nome), f"{path.name}: {nome}")
            self.assertFalse(_ignorado(padroes, ".env.example"), path)

    def test_copia_do_template_igual_a_raiz(self):
        self.assertEqual(IGNORES[0].read_text(encoding="utf-8"), IGNORES[1].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
