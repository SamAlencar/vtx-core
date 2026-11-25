"""VTX-175: política de isolamento e projects/ sem código/dados de cliente."""
from __future__ import annotations

import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
PROJECTS = RAIZ / "projects"
DOC = RAIZ / "knowledge/seguranca/isolamento-clientes.md"
AGENTS = RAIZ / "agents"

# Sandbox de ferramenta da VTX (não é repositório de cliente).
SANDBOX_PREFIXO = "sandbox-"
# Documentação ainda no core, a migrar; não pode ganhar código nem segredo.
LEGADO = {"med-hub", "plataforma-projetos"}
# Ponteiro e metadados públicos permitidos em pasta de cliente.
META = {".gitkeep", "readme.md", "conexoes.yaml", "conexoes.yml"}

CODIGO = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".vue", ".svelte",
    ".go", ".rs", ".java", ".kt", ".cs", ".cpp", ".c", ".rb", ".php",
    ".swift", ".sh", ".ipynb",
}
# Diagramas versionados no legado (Mermaid renderizado).
DIAGRAMA = {".html", ".svg", ".png", ".jpg", ".jpeg", ".webp"}
SEGREDO_NOMES = {".env", ".env.local", ".pem", ".p12", "id_rsa", "credentials.json"}
DADOS = {".db", ".sqlite", ".sqlite3", ".dump", ".sql", ".csv"}


def _pastas_projeto() -> list[Path]:
    if not PROJECTS.is_dir():
        return []
    return sorted(
        p for p in PROJECTS.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )


class TestIsolamentoClientes(unittest.TestCase):
    def test_documento_e_indice(self):
        self.assertTrue(DOC.is_file())
        texto = DOC.read_text(encoding="utf-8")
        for trecho in (
            "um repositório por cliente",
            "segredos",
            "ponteiro",
            "projects/",
        ):
            self.assertIn(trecho, texto.lower() if trecho != "projects/" else texto)
        index = (RAIZ / "knowledge/INDEX.md").read_text(encoding="utf-8")
        self.assertIn("seguranca/isolamento-clientes.md", index)
        readme = (PROJECTS / "README.md").read_text(encoding="utf-8")
        self.assertIn("isolamento-clientes.md", readme)
        self.assertIn("repositório próprio", readme)

    def test_papeis_nao_dao_leitura_irrestrita(self):
        for path in sorted(AGENTS.glob("*.md")):
            texto = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "leitura em todo o repositório",
                texto,
                path.name,
            )
            self.assertNotIn(
                "leitura do resto",
                texto,
                path.name,
            )

    def test_projects_sem_codigo_nem_segredo_de_cliente(self):
        falhas = []
        for pasta in _pastas_projeto():
            nome = pasta.name
            for path in pasta.rglob("*"):
                if not path.is_file():
                    continue
                rel = path.relative_to(PROJECTS).as_posix()
                partes = set(path.parts)
                if ".git" in partes or "tmp-repo" in partes or "node_modules" in partes:
                    continue
                baixo = path.name.lower()
                suf = path.suffix.lower()
                if baixo in SEGREDO_NOMES or (baixo.startswith(".env") and baixo != ".env.example"):
                    falhas.append(f"{rel}: segredo não pode estar no vtx-core")
                    continue
                if suf in DADOS:
                    falhas.append(f"{rel}: dado operacional não pode estar no vtx-core")
                    continue
                if nome.startswith(SANDBOX_PREFIXO):
                    continue
                if suf in CODIGO:
                    falhas.append(f"{rel}: código de cliente/produto não fica em projects/")
                    continue
                if nome in LEGADO:
                    if suf not in {".md"} | DIAGRAMA and baixo not in META:
                        falhas.append(
                            f"{rel}: no legado só documentação (.md) e diagrama"
                        )
                    continue
                # Pasta nova de cliente: só ponteiro e metadados.
                if baixo not in META and suf != ".md":
                    falhas.append(
                        f"{rel}: em pasta que não é legado nem sandbox, só README/metadados"
                    )
        self.assertEqual(falhas, [])


if __name__ == "__main__":
    unittest.main()
