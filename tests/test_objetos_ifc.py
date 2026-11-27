"""Testes da camada de objetos IFC <-> JSON (VTX-152, parte 1)."""
import json
import pathlib
import tempfile
import unittest

TEK_MODEL = pathlib.Path("/workspace/repos/tekto-model/tests/dados/catalogo_parede_exemplo.ifc")
from importlib.resources import files as _files

from vtx_ifc import objetos, receitas

EXEMPLO_IDS = pathlib.Path(_files("vtx_ifc").joinpath("exemplo.ids"))

try:
    import ifcopenshell
    import ifcopenshell.api.group
    import ifcopenshell.api.material
    import ifcopenshell.api.type
    import ifcopenshell.validate
    import ifctester  # noqa: F401
    TEM = True
except ImportError:
    TEM = False


def mod(nome):
    return receitas if nome == "receitas" else objetos


@unittest.skipUnless(TEM, "ifcopenshell/ifctester não instalados")
class TestObjetos(unittest.TestCase):
    def setUp(self):
        self.r, self.o = mod("receitas"), mod("objetos")
        api = ifcopenshell.api
        f = self.f = self.r.criar_modelo()
        predio = f.by_type("IfcBuilding")[0]
        self.andar2 = api.root.create_entity(f, ifc_class="IfcBuildingStorey", name="Pav 2")
        api.aggregate.assign_object(f, products=[self.andar2], relating_object=predio)
        tipo = api.root.create_entity(f, ifc_class="IfcWallType", name="Bloco 14")
        cam = api.material.add_material_set(f, name="Bloco 14", set_type="IfcMaterialLayerSet")
        for nome, esp in (("Reboco", 20.0), ("Bloco", 140.0)):
            api.material.add_layer(f, layer_set=cam, material=api.material.add_material(f, name=nome)).LayerThickness = esp
        api.material.assign_material(f, products=[tipo], material=cam)
        self.p1 = self.r.criar_parede(f, "P1", 4, 0.18, 3, {"Pset_WallCommon": {"IsExternal": True}})
        api.type.assign_type(f, related_objects=[self.p1], relating_type=tipo)
        self.p2 = self.r.criar_parede(f, "P2", 2, 0.15, 3)  # sem tipo, sem material, sem grupo
        self.grupo = api.group.add_group(f, name="Fachada norte")
        api.group.assign_group(f, products=[self.p1], group=self.grupo)

    def por_id(self, objs):
        return {x["globalid"]: x for x in objs}

    def test_camada_sem_material_mantem_posicao(self):
        api = ifcopenshell.api
        cam = api.material.add_material_set(self.f, name="Misto", set_type="IfcMaterialLayerSet")
        api.material.add_layer(self.f, layer_set=cam, material=api.material.add_material(self.f, name="Reboco"))
        vazia = api.material.add_layer(self.f, layer_set=cam, material=api.material.add_material(self.f, name="tmp"))
        vazia.Material = None
        api.material.assign_material(self.f, products=[self.p2], material=cam)
        b = self.por_id(self.o.extrair(self.f))[self.p2.GlobalId]
        self.assertEqual(b["materiais"], ["Reboco", None])

    def test_extrai_campos(self):
        o = self.por_id(self.o.extrair(self.f))
        a, b = o[self.p1.GlobalId], o[self.p2.GlobalId]
        self.assertEqual((a["classe"], a["nome"], a["tipo"]["nome"], a["andar"]["nome"]), ("IfcWall", "P1", "Bloco 14", "Terreo"))
        self.assertEqual(a["materiais"], ["Reboco", "Bloco"])
        self.assertEqual(a["grupos"][0]["nome"], "Fachada norte")
        self.assertIs(a["psets"]["Pset_WallCommon"]["IsExternal"], True)
        self.assertEqual((b["tipo"], b["materiais"], b["grupos"]), (None, [], []))
        json.dumps(list(o.values()))  # serializável para jsonb

    def test_ida_e_volta_sem_edicao_idempotente(self):
        antes = self.o.extrair(self.f)
        res = self.o.aplicar(self.f, json.loads(json.dumps(antes)))
        self.assertEqual((res["alterados"], res["erros"]), (0, []))
        with tempfile.TemporaryDirectory() as d:
            self.f.write(f"{d}/v.ifc")
            g = ifcopenshell.open(f"{d}/v.ifc")
        self.assertEqual(self.o.extrair(g), antes)

    def test_edicao_volta_para_o_ifc(self):
        objs = self.por_id(self.o.extrair(self.f))
        x = objs[self.p2.GlobalId]
        x["nome"] = "P2-editada"
        x["psets"]["Pset_WallCommon"] = {"IsExternal": False, "LoadBearing": True}
        x["andar"] = {"globalid": self.andar2.GlobalId}
        x["grupos"] = [{"globalid": self.grupo.GlobalId}]
        res = self.o.aplicar(self.f, list(objs.values()))
        self.assertEqual((res["alterados"], res["erros"]), (1, []))
        y = self.por_id(self.o.extrair(self.f))[self.p2.GlobalId]
        self.assertEqual((y["nome"], y["andar"]["nome"], y["grupos"][0]["nome"]), ("P2-editada", "Pav 2", "Fachada norte"))
        self.assertIs(y["psets"]["Pset_WallCommon"]["LoadBearing"], True)
        self.assertEqual(self.p2.GlobalId, y["globalid"])
        logger = ifcopenshell.validate.json_logger()
        ifcopenshell.validate.validate(self.f, logger)
        self.assertEqual(logger.statements, [])

    def test_globalid_inexistente_vira_erro(self):
        res = self.o.aplicar(self.f, [{"globalid": "0000000000000000000000", "nome": "x"}])
        self.assertEqual(res["alterados"], 0)
        self.assertIn("globalid_inexistente", res["erros"][0]["codigo"])

    def test_ids_reprova_depois_de_tirar_isexternal(self):
        def ids():
            with tempfile.TemporaryDirectory() as d:
                self.f.write(f"{d}/v.ifc")
                return self.r.validar_ids(f"{d}/v.ifc", EXEMPLO_IDS)["aprovado"]
        objs = self.por_id(self.o.extrair(self.f))
        objs[self.p2.GlobalId]["psets"]["Pset_WallCommon"] = {"IsExternal": False}
        self.o.aplicar(self.f, list(objs.values()))
        self.assertTrue(ids())
        objs = self.por_id(self.o.extrair(self.f))
        objs[self.p1.GlobalId]["psets"]["Pset_WallCommon"].pop("IsExternal")
        self.o.aplicar(self.f, list(objs.values()))
        self.assertFalse(ids())

    @unittest.skipUnless(TEK_MODEL.exists(), "tekto-model não clonado (só local)")
    def test_tipo_do_tek_model(self):
        tipos = self.o.extrair(ifcopenshell.open(str(TEK_MODEL)), classe="IfcElementType")
        self.assertEqual(tipos[0]["materiais"], ["Reboco exemplo", "Bloco exemplo", "Reboco exemplo"])
        self.assertIs(tipos[0]["psets"]["Pset_WallCommon"]["IsExternal"], False)


if __name__ == "__main__":
    unittest.main()
