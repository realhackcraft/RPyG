import unittest

from classes.map import Structure


class TestStructure(unittest.TestCase):
    def setUp(self) -> None:
        self.structure = Structure("tests/assets/structure.txt")

    def test_load_structure(self):
        return None
