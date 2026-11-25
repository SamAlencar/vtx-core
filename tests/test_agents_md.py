"""VTX-169: caminhos citados no AGENTS.md e nas regras por papel existem."""
from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]

ARQUIVOS = [
    RAIZ / "AGENTS.md",
    RAIZ / ".cursor/rules/papeis/planejamento.mdc",
    RAIZ / ".cursor/rules/papeis/execucao.mdc",
]

RE_LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
RE_TICK = re.compile(r"`([^`]+)`")

# Placeholders, globs e comandos não são arquivos deste repositório.
RE_PULAR = re.compile(r"[<>*]|\{")


def _eh_externo(url: str) -> bool:
    return url.lower().startswith(("http://", "https://", "mailto:", "tel:", "data:"))


def _parece_caminho(texto: str) -> bool:
    if not texto or RE_PULAR.search(texto):
        return False
    if " " in texto or texto.startswith("-"):
        return False
    if texto in {"globs", "alwaysApply", "false", "true", "pt-BR"}:
        return False
    return ("/" in texto) or Path(texto).suffix in {
        ".md", ".mdc", ".yml", ".yaml", ".py", ".sh", ".json",
    } or texto.endswith("/")


def caminhos_de(path: Path) -> list[tuple[str, Path]]:
    texto = path.read_text(encoding="utf-8")
    encontrados: list[tuple[str, Path]] = []
    vistos: set[str] = set()

    def registrar(bruto: str, relativo_ao_arquivo: bool) -> None:
        url = bruto.split()[0].strip().rstrip(".,;")
        if not url or url.startswith("#") or _eh_externo(url):
            return
        url = url.split("#", 1)[0]
        if not url or not _parece_caminho(url) or url in vistos:
            return
        vistos.add(url)
        if relativo_ao_arquivo:
            alvo = (path.parent / url).resolve()
        else:
            alvo = (RAIZ / url).resolve()
        encontrados.append((url, alvo))

    for bruto in RE_LINK.findall(texto):
        registrar(bruto, relativo_ao_arquivo=True)
    for bruto in RE_TICK.findall(texto):
        registrar(bruto, relativo_ao_arquivo=False)
    return encontrados


class TestAgentsMd(unittest.TestCase):
    def test_arquivos_existem(self):
        for path in ARQUIVOS:
            self.assertTrue(path.is_file(), f"ausente: {path.relative_to(RAIZ)}")

    def test_agents_md_tem_ate_cerca_de_60_linhas(self):
        linhas = (RAIZ / "AGENTS.md").read_text(encoding="utf-8").splitlines()
        self.assertLessEqual(len(linhas), 60, f"AGENTS.md tem {len(linhas)} linhas")
        self.assertGreaterEqual(len(linhas), 20)

    def test_ponteiros_obrigatorios(self):
        texto = (RAIZ / "AGENTS.md").read_text(encoding="utf-8")
        for trecho in (
            "knowledge/processos/fluxo-entre-agentes.md",
            "knowledge/processos/governanca-e-aprovacoes.md",
            "knowledge/INDEX.md",
            "agents/",
            "A0",
            "A3",
        ):
            self.assertIn(trecho, texto)

    def test_regras_sao_opt_in(self):
        for path in ARQUIVOS[1:]:
            texto = path.read_text(encoding="utf-8")
            self.assertIn("alwaysApply: false", texto)
            self.assertIn("globs:", texto)
            self.assertNotIn("alwaysApply: true", texto)
            # O Cursor separa globs por vírgula; chaves com vírgula quebram o padrão.
            for linha in texto.splitlines():
                if linha.startswith("globs:"):
                    self.assertNotIn("{", linha, path.name)

    def test_caminhos_citados_existem(self):
        falhas = []
        for path in ARQUIVOS:
            for url, alvo in caminhos_de(path):
                try:
                    alvo.relative_to(RAIZ)
                except ValueError:
                    # Path fora do repo (ex.: subida demais) — ainda assim precisa existir? Não.
                    falhas.append(f"{path.relative_to(RAIZ)}: {url} sai do repositório")
                    continue
                if not alvo.exists():
                    no_template = (RAIZ / "templates" / "projeto" / url).resolve()
                    if no_template.exists():
                        continue
                    falhas.append(f"{path.relative_to(RAIZ)}: caminho ausente {url}")
        self.assertEqual(falhas, [])


if __name__ == "__main__":
    unittest.main()
