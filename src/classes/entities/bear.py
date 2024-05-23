"""
The bear entity
"""

import random

from typing import Any

from classes.entities.entity import Entity
from classes.map import Map
from utils.math import Math


class Bear(Entity):
    def __init__(self, x: int, y: int) -> None:
        super().__init__("Bear", "B", x, y, 5)
        self.damage = 2

    def tick(self, *args: Any):
        player = args[0]
        game_map = args[1]

        # if type(player) is not Player:
        #     return

        if not isinstance(game_map, Map):
            return

        if Math.distance((player.x, player.y), (self.x, self.y)) > 5:
            self.x += random.randint(-1, 1)
            self.y += random.randint(-1, 1)
            # Check if the bear is now out of bound (BOoB)
            if self.y >= len(game_map):
                self.y = len(game_map) - 1
            elif self.y < 0:
                self.y = 0

            if self.x >= len(game_map[self.y]):
                self.x = len(game_map[self.y]) - 1
            elif self.x < 0:
                self.x = 0
            # Check dist beteewn player and self is greater than 5
        elif self.x == player.x and self.y == player.y:
            player.health -= self.damage
        else:
            # Simulate bear movement
            left_x = Math.distance((player.x, player.y), (self.x - 1, self.y))
            right_x = Math.distance((player.x, player.y), (self.x + 1, self.y))
            up_y = Math.distance((player.x, player.y), (self.x, self.y - 1))
            down_y = Math.distance((player.x, player.y), (self.x, self.y + 1))

            # Find movment that will give minimum distance to the player
            minimum_distance = min(left_x, right_x, up_y, down_y)

            # Move
            multiplier = 1
            if random.getrandbits(3) == 0:
                multiplier = 0

            if minimum_distance == left_x:
                self.x -= multiplier * 1
            elif minimum_distance == right_x:
                self.x += multiplier * 1
            elif minimum_distance == up_y:
                self.y -= multiplier * 1
            else:
                self.y += multiplier * 1
