"""
The map class for the game map
"""

import os
from copy import deepcopy
from typing import List

from classes.entity import Entity
from classes.player import Player
from classes.structure import Structure
from utils.displayManager import DisplayManager
from utils.file import FileUtils


class Map:
    def __init__(self, path: str, dm: DisplayManager, loadPath: bool = True):
        self.path = path
        self.game_map: List[List[str]] = []
        self.color_dict = {}
        self.entities = []
        self.loaded_up = self.loaded_down = self.loaded_left = self.loaded_right = None

        up = down = left = right = colors = structures = None

        with open(path, "r") as file:
            for i, line in enumerate(file):
                if i == 0:
                    up, down, left, right, colors, structures = self.parse_map_header(
                        line
                    )
                    continue
                self.game_map.append(line.split())
            if colors:
                self.color_dict = FileUtils.parse_colors(colors)
        self.dm = dm

        self.up = up
        self.down = down
        self.left = left
        self.right = right

        self.structures = structures
        if loadPath:
            self.load_path()

    def load_path(self):
        if self.up:
            self.loaded_up = Map(self.up, self.dm, False)
        if self.down:
            self.loaded_down = Map(self.down, self.dm, False)
        if self.left:
            self.loaded_left = Map(self.left, self.dm, False)
        if self.right:
            self.loaded_right = Map(self.right, self.dm, False)
        if self.structures:
            self.loaded_structures = []
            for structure in self.structures:
                self.loaded_structures.append(Structure(structure))

    def render_map(self, player: Player, entities: List[Entity], last_user_input: str):
        self.display_map = deepcopy(self.game_map)

        for e in entities:
            self.display_map[e.y][e.x] = e.symbol

        self.display_map[player.y][player.x] = player.symbol

        self.print_under(entities, player)
        self.print_stats(player, last_user_input)
        self.print_map()

    def print_map(self):
        for row in self.display_map:
            self.dm.add_to_buffer(
                " ".join([f"{self.color_dict[tile]}{tile}\033[0m" for tile in row])
            )

    def print_stats(self, player: Player, last_user_input: str):
        p = player
        user_input = last_user_input.upper()
        self.dm.add_to_buffer("-" * os.get_terminal_size().columns)
        stats = f"Hunger: {p.hunger}/{p.max_hunger}, Thirst: {p.thirst}/{p.max_thirst}, Last Input: {user_input}"
        self.dm.add_to_buffer(stats)
        self.dm.add_to_buffer("-" * os.get_terminal_size().columns)

    def print_under(self, entities: List[Entity], player: Player):
        self.dm.add_to_buffer("-" * os.get_terminal_size().columns)
        display_text = f"Block: {self.game_map[player.y][player.x]}, Entities: "
        for e in entities:
            if e.y == player.y and e.x == player.x:
                display_text += f"{e.name}, "
        self.dm.add_to_buffer(display_text.rstrip(", "))

    @staticmethod
    def parse_map_header(text: str):
        args = text.split(", ")  # Split the arguments with comma and space
        up = down = left = right = colors = structures = None

        for arg in args:
            name = arg[0]  # Name of the arg
            arg = arg[3:].strip()  # Arg after the name, colon and space
            match name:
                case "U":
                    up = arg
                case "D":
                    down = arg
                case "L":
                    left = arg
                case "R":
                    right = arg
                case "C":
                    colors = arg
                case "I":
                    structures = arg.split(": ")

        return [up, down, left, right, colors, structures]

    def __getitem__(self, index: int):
        return self.game_map[index]

    def __len__(self):
        return len(self.game_map)
