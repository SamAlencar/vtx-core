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
    "Read(**/.env.development)",
    "Read(**/.env.test)",
    "Read(**/*.pem)",
    "Read(**/*.key)",
    "Read(**/*.p12)",
    "Read(**/*.pfx)",
    "Read(~/.ssh/**)",
    "Write(**/.env)",
    "Write(**/.env.development)",
    "Write(**/.env.test)",
    "Write(**/*.key)",
    "Write(**/*.p12)",
    "Write(**/*.pfx)",
    "Shell(sudo)",
    "Shell(rm:-rf *)",
    "Shell(rm:-R*)",
    "Shell(rm:-r*)",
    "Shell(rm:*--recursive*)",
    "Shell(rm:* -r*)",
    "Shell(rm:-fR*)",
    "Shell(rm:* -R*)",
    "Shell(find:* -delete*)",
    "Shell(find:-delete*)",
    "Shell(git:push --force)",
    "Shell(git:push * --force *)",
    "Shell(git:push -f *)",
    "Shell(git:push * main)",
    "Shell(git:push *:main)",
    "Shell(git:push *refs/heads/main)",
    "Shell(git:push *refs/heads/main:*)",
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


def _padroes_shell(deny: list[str], prefixo: str) -> list[str]:
    return [r[len(prefixo):-1] for r in deny if r.startswith(prefixo) and r.endswith(")")]


def _casa(comando: str, padroes: list[str]) -> bool:
    return any(fnmatch.fnmatchcase(comando, p) for p in padroes)


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
        padroes = _padroes_shell(_deny(CLI.read_text(encoding="utf-8")), "Shell(git:")
        self.assertFalse(_casa(comando, padroes))
        self.assertTrue(_casa("push --force origin main", padroes))

    def test_push_para_main_por_refspec_e_bloqueado(self):
        # Contornos apontados na revisão do Tzu (PR #28): main:main, HEAD:refs/heads/main, refs/heads/main.
        # Aproximação com fnmatch; não é o motor do CLI.
        padroes = _padroes_shell(_deny(CLI.read_text(encoding="utf-8")), "Shell(git:")
        for comando in (
            "push origin main:main",
            "push origin HEAD:refs/heads/main",
            "push origin refs/heads/main",
            "push origin HEAD:main",
            "push origin main",
        ):
            self.assertTrue(_casa(comando, padroes), comando)
        # Branch de PR e nomes que só começam com main (main-hotfix, maintenance) continuam liberados.
        # git push sem argumentos não casa (limite documentado no §8).
        for comando in (
            "push origin vtx-224-deny-rules-cursor",
            "push origin main-hotfix",
            "push origin HEAD:main-hotfix",
            "push origin HEAD:refs/heads/main-hotfix",
            "push origin refs/heads/main-hotfix",
            "push origin refs/heads/maintenance",
            "push",
        ):
            self.assertFalse(_casa(comando, padroes), comando)

    def test_rm_recursivo_e_find_delete_sao_bloqueados(self):
        # Contornos apontados na revisão do Tzu (PR #28): -Rf, -r -f, --recursive, find -delete.
        rm = _padroes_shell(_deny(CLI.read_text(encoding="utf-8")), "Shell(rm:")
        for args in (
            "-rf /tmp/x",
            "-fr /tmp/x",
            "-r /tmp/x",
            "-Rf /tmp/x",
            "-r -f /tmp/x",
            "--recursive /tmp/x",
            "-f -r /tmp/x",
            "-fR /tmp/x",
            "-f -R /tmp/x",
        ):
            self.assertTrue(_casa(args, rm), args)
        self.assertFalse(_casa("-f arquivo.txt", rm))
        find = _padroes_shell(_deny(CLI.read_text(encoding="utf-8")), "Shell(find:")
        self.assertTrue(_casa(". -name foo -delete", find))
        self.assertTrue(_casa("-delete", find))
        self.assertFalse(_casa(". -type f", find))

    def test_cursorignore_esconde_segredos_e_mostra_exemplo(self):
        for path in IGNORES:
            padroes = _ativos(path)
            for nome in (
                ".env",
                ".env.local",
                ".env.production",
                ".env.development",
                ".env.test",
                "servidor.pem",
                "privada.key",
                "id_ed25519",
                ".npmrc",
            ):
                self.assertTrue(_ignorado(padroes, nome), f"{path.name}: {nome}")
            self.assertFalse(_ignorado(padroes, ".env.example"), path)

    def test_copia_do_template_igual_a_raiz(self):
        self.assertEqual(IGNORES[0].read_text(encoding="utf-8"), IGNORES[1].read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
