"""Testes do padrão de funções de domínio para tool-calling (VTX-146)."""
import importlib.util, json, pathlib, sys, unittest

RAIZ = pathlib.Path(__file__).resolve().parent.parent / ".cursor/skills/ifc-python"
try:
    import ifcopenshell  # noqa: F401
    import ifcopenshell.geom
    import ifcopenshell.util.element
    import jsonschema  # noqa: F401
    TEM = True
except ImportError:
    TEM = False


def carregar():
    sys.path.insert(0, str(RAIZ))
    spec = importlib.util.spec_from_file_location("funcoes", RAIZ / "funcoes.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@unittest.skipUnless(TEM, "ifcopenshell/jsonschema não instalados")
class TestFuncoesDominio(unittest.TestCase):
    def setUp(self):
        self.fn = carregar()
        self.f = self.fn.receitas.criar_modelo()

    def parede(self):
        r = self.fn.chamar(self.f, "criar_parede", {"nome": "P1", "comprimento_mm": 5000,
                                                     "espessura_mm": 150, "altura_mm": 2800, "externa": True})
        self.assertTrue(r["ok"], r)
        return r["resultado"]["GlobalId"]

    def test_criar_parede_em_mm(self):
        gid = self.parede()
        w = self.f.by_guid(gid)
        self.assertEqual(w.is_a(), "IfcWall")
        self.assertTrue(ifcopenshell.util.element.get_psets(w)["Pset_WallCommon"]["IsExternal"])

    def test_abrir_vao(self):
        gid = self.parede()
        r = self.fn.chamar(self.f, "abrir_vao", {"parede": gid, "largura_mm": 900, "altura_mm": 2100,
                                                 "peitoril_mm": 0, "posicao_mm": 1000})
        self.assertTrue(r["ok"], r)
        self.assertEqual(len(self.f.by_type("IfcRelVoidsElement")), 1)

    def test_vao_em_parede_inexistente(self):
        r = self.fn.chamar(self.f, "abrir_vao", {"parede": "0" * 22, "largura_mm": 900, "altura_mm": 2100,
                                                 "peitoril_mm": 0, "posicao_mm": 0})
        self.assertEqual(r["erro"]["codigo"], "ELEMENTO_NAO_ENCONTRADO")

    def test_vao_maior_que_parede(self):
        gid = self.parede()
        r = self.fn.chamar(self.f, "abrir_vao", {"parede": gid, "largura_mm": 900, "altura_mm": 2100,
                                                 "peitoril_mm": 0, "posicao_mm": 4500})
        self.assertEqual(r["erro"]["codigo"], "REGRA_VIOLADA")

    def test_pilar_altura_negativa(self):
        r = self.fn.chamar(self.f, "lancar_pilar", {"nome": "P1", "largura_mm": 200, "profundidade_mm": 400,
                                                    "altura_mm": -1, "x_mm": 0, "y_mm": 0})
        self.assertFalse(r["ok"])
        self.assertEqual(r["erro"]["codigo"], "PARAMETRO_INVALIDO")
        self.assertEqual(r["erro"]["campo"], "altura_mm")

    def test_pilar_ok_e_campo_extra(self):
        ok = self.fn.chamar(self.f, "lancar_pilar", {"nome": "P1", "largura_mm": 200, "profundidade_mm": 400,
                                                     "altura_mm": 2800, "x_mm": 1000, "y_mm": 0})
        self.assertTrue(ok["ok"], ok)
        sh = ifcopenshell.geom.create_shape(ifcopenshell.geom.settings(), self.f.by_guid(ok["resultado"]["GlobalId"]))
        xs, ys, zs = sh.geometry.verts[0::3], sh.geometry.verts[1::3], sh.geometry.verts[2::3]
        self.assertAlmostEqual(max(xs) - min(xs), 0.2, places=4)  # geometria em metro: 200 mm
        self.assertAlmostEqual(max(ys) - min(ys), 0.4, places=4)
        self.assertAlmostEqual(max(zs) - min(zs), 2.8, places=4)
        extra = self.fn.chamar(self.f, "lancar_pilar", {"nome": "P2", "largura_mm": 200, "profundidade_mm": 400,
                                                        "altura_mm": 2800, "x_mm": 0, "y_mm": 0, "fck": 30})
        self.assertEqual(extra["erro"]["codigo"], "PARAMETRO_INVALIDO")

    def test_funcao_desconhecida_e_ferramentas(self):
        self.assertEqual(self.fn.chamar(self.f, "demolir", {})["erro"]["codigo"], "FUNCAO_DESCONHECIDA")
        tools = self.fn.ferramentas()
        self.assertEqual({t["name"] for t in tools}, {"criar_parede", "abrir_vao", "lancar_pilar"})
        json.dumps(tools)  # serializável para a API da IA


if __name__ == "__main__":
    unittest.main()
