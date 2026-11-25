import unittest, yaml, pathlib

CAMPOS = {"id", "nome", "area", "tipo", "link", "licenca", "status", "uso_agentes", "riscos", "responsavel", "revisado_em"}
STATUS = {"em avaliação", "adotado", "adotado com restrições", "descartado"}
TIPOS = {"skill", "regras", "mcp", "componentes", "referência", "lista"}


class TestRecursos(unittest.TestCase):
    def test_registro_valido(self):
        caminho = pathlib.Path(__file__).resolve().parent.parent / "knowledge/ferramentas/recursos.yaml"
        itens = yaml.safe_load(caminho.read_text(encoding="utf-8"))["recursos"]
        ids = [r["id"] for r in itens]
        self.assertEqual(len(ids), len(set(ids)))
        for r in itens:
            self.assertTrue(CAMPOS <= set(r), r["id"])
            self.assertIn(r["status"], STATUS, r["id"])
            self.assertIn(r["tipo"], TIPOS, r["id"])
            self.assertTrue(str(r["link"]).startswith("https://"), r["id"])


if __name__ == "__main__":
    unittest.main()
