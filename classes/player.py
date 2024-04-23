from collections import OrderedDict

from classes.entity import Entity


class Player(Entity):
  def __init__(self, x: int, y: int):
    super().__init__("Player", "@", x, y, 5)
    self.hunger = 3
    self.thirst = 3
    self.max_hunger = 10
    self.max_thirst = 10
    self.inventory = OrderedDict()
    
    self.inventory["wood"] = 0

  def set_hunger(self, hunger: int) -> bool:
    if hunger > self.max_hunger:
      self.hunger = self.max_hunger
      return False
    self.hunger = hunger
    return True

  def set_thirst(self, thirst: int) -> bool:
    if thirst > self.max_thirst:
      self.thirst = self.max_thirst
      return False
    self.thirst = thirst
    return True   
