import unittest

from classes.map import Map
from utils.displayManager import DisplayManager


class TestMap(unittest.TestCase):
    def setUp(self) -> None:
        self.dm = DisplayManager()
        self.game_map = Map("tests/assets/map.txt", self.dm)

    def test_create_map(self) -> None:
        return None
