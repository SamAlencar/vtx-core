import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hello import hello


class TestHello(unittest.TestCase):
    def test_padrao(self):
        self.assertEqual(hello(), "Olá, mundo!")

    def test_nome(self):
        self.assertEqual(hello("VTX"), "Olá, VTX!")


if __name__ == "__main__":
    unittest.main()
