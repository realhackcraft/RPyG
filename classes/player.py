from classes.entity import Entity


class Player(Entity):
  def __init__(self, x: int, y: int):
    super().__init__("Player", "@", x, y, 5)
    self.hunger = 3
    self.thrist = 3
    self.inventory = {"wood": 0}
