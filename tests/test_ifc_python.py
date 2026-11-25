"""Testes da skill .cursor/skills/ifc-python (VTX-145)."""
import pathlib, tempfile, unittest

try:
    import ifcopenshell  # noqa: F401
    import ifctester  # noqa: F401
    from importlib.resources import files as _files
    from vtx_ifc import receitas as _receitas
    EXEMPLO_IDS = pathlib.Path(_files("vtx_ifc").joinpath("exemplo.ids"))
    TEM_IFC = True
except ImportError:
    TEM_IFC = False
    _receitas = None
    EXEMPLO_IDS = None


def carregar():
    return _receitas


@unittest.skipUnless(TEM_IFC, "ifcopenshell/ifctester não instalados")
class TestIfcPython(unittest.TestCase):
    def setUp(self):
        self.r = carregar()
        self.tmp = pathlib.Path(tempfile.mkdtemp())

    def _salvar(self, f, nome):
        caminho = self.tmp / nome
        f.write(str(caminho))
        return caminho

    def test_criar_ler_reabrir(self):
        f = self.r.criar_modelo()
        self.r.criar_parede(f, "P1", 5.0, 0.2, 3.0, {"Pset_WallCommon": {"IsExternal": True}})
        g = ifcopenshell.open(str(self._salvar(f, "a.ifc")))
        self.assertEqual(g.schema, "IFC4")
        paredes = self.r.listar(g, "IfcWall")
        self.assertEqual(len(paredes), 1)
        self.assertEqual(paredes[0]["nome"], "P1")
        psets = self.r.ler_psets(g.by_guid(paredes[0]["GlobalId"]))
        self.assertIs(psets["Pset_WallCommon"]["IsExternal"], True)

    def test_sem_pset_devolve_vazio(self):
        f = self.r.criar_modelo()
        p = self.r.criar_parede(f, "P2", 2.0, 0.1, 2.5)
        self.assertEqual(self.r.ler_psets(p), {})

    def test_listar_ifc2x3(self):
        f = ifcopenshell.file(schema="IFC2X3")
        f.createIfcWall(ifcopenshell.guid.new(), None, "Antiga")
        self.assertEqual([p["nome"] for p in self.r.listar(f, "IfcWall")], ["Antiga"])

    def test_validar_ids(self):
        ids = EXEMPLO_IDS
        f = self.r.criar_modelo()
        self.r.criar_parede(f, "Ext", 5.0, 0.2, 3.0, {"Pset_WallCommon": {"IsExternal": True}})
        ok = self.r.validar_ids(self._salvar(f, "ok.ifc"), ids)
        self.assertTrue(ok["aprovado"])
        f2 = self.r.criar_modelo()
        self.r.criar_parede(f2, "SemPset", 5.0, 0.2, 3.0)
        ruim = self.r.validar_ids(self._salvar(f2, "ruim.ifc"), ids)
        self.assertFalse(ruim["aprovado"])
        self.assertTrue(ruim["especificacoes"])

    def test_diff_por_globalid(self):
        a = self.r.criar_modelo()
        self.r.criar_parede(a, "P1", 5.0, 0.2, 3.0, {"Pset_WallCommon": {"IsExternal": False}})
        b = ifcopenshell.open(str(self._salvar(a, "v1.ifc")))
        parede = b.by_type("IfcWall")[0]
        self.r.definir_pset(b, parede, {"Pset_WallCommon": {"IsExternal": True}})
        self.r.criar_parede(b, "P2", 3.0, 0.15, 3.0)
        d = self.r.diff_por_globalid(a, b)
        self.assertEqual(len(d["adicionados"]), 1)
        self.assertEqual(d["removidos"], [])
        self.assertEqual([x["GlobalId"] for x in d["alterados"]], [parede.GlobalId])


if __name__ == "__main__":
    unittest.main()
