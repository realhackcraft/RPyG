from collections.abc import MutableSet
import random
import math

from classes.entity import Any, Entity
from classes.player import Player
from utils.math import Math


class Bear(Entity):
  def __init__(self, x: int, y: int):
    super().__init__("Bear", "B", x, y, 5)
    self.damage = 2
  
  def tick(self, *args: Any):
    player = args[0]
    if type(player) is not Player:
      return

    if self.x == player.x and self.y == player.y:
      player.health -= self.damage
      # check dist beteewn player and self is greater than 5
    elif Math.distance((player.x, player.y), (self.x, self.y)) > 5:
      self.x += random.randint(-1, 1)
      self.y += random.randint(-1, 1)
    else:
      left_x = Math.distance((player.x, player.y), (self.x - 1, self.y))
      right_x = Math.distance((player.x, player.y), (self.x + 1, self.y))
      up_y = Math.distance((player.x, player.y), (self.x, self.y - 1))
      down_y = Math.distance((player.x, player.y), (self.x, self.y + 1))

      minimum_distance = min(left_x, right_x, up_y, down_y)

      if minimum_distance == left_x:
        self.x -= 1
      elif minimum_distance == right_x:
        self.x += 1
      elif minimum_distance == up_y:
        self.y -= 1
      else:
        self.y += 1
