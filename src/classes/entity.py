from abc import abstractmethod
from typing import Any

"""
The base class for all entities
"""
class Entity:
  def __init__(self, name: str, symbol: str, x: int, y: int, health: int):
    self.name = name
    self.symbol = symbol
    self.x = x
    self.y = y
    self.health = health
  
  def tick(self, *args: Any):
    pass
