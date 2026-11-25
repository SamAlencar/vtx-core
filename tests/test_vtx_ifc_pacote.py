"""VTX-176: o núcleo IFC instala como pacote e importa sem sys.path."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path


class TestVtxIfcPacote(unittest.TestCase):
    def test_importa_sem_manipular_sys_path(self):
        antes = list(sys.path)
        import vtx_ifc
        from vtx_ifc import funcoes, objetos, receitas
        self.assertEqual(sys.path, antes)
        self.assertTrue(hasattr(funcoes, "chamar"))
        self.assertTrue(hasattr(objetos, "extrair"))
        self.assertTrue(hasattr(receitas, "criar_modelo"))
        raiz = Path(vtx_ifc.__file__).resolve().parents[1]
        self.assertEqual(raiz.name, "core")

    def test_exemplo_ids_no_pacote(self):
        from importlib.resources import files
        path = Path(files("vtx_ifc").joinpath("exemplo.ids"))
        self.assertTrue(path.is_file())
        self.assertIn("ids", path.read_text(encoding="utf-8")[:200].lower())


if __name__ == "__main__":
    unittest.main()
