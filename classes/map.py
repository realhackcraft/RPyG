from typing import List

import os

from copy import deepcopy

from utils.displayManager import DisplayManager
from classes.entity import Entity
from classes.player import Player

class Map:
  def __init__(self, path: str, dm: DisplayManager):
    print("\033[=3h")  # Set display mode to 80x25 with color support
    game_map: List[List[str]] = []
    color_dict = {}

    with open(path, "r") as file:
      for i, line in enumerate(file):
        if i == 0:
          up, down, left, right, colors = self.parse_map_header(line)
          continue
        game_map.append(line.split())
  
      with open(colors, 'r') as color_file:
        for line in color_file:
          key, value = line.strip().split(' ')
          color_dict[key] = f"\033[{value}m"

    self.dm = dm
    self.game_map = game_map
    self.color_dict = color_dict
    self.up = up
    self.down = down
    self.left = left
    self.right = right

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
      self.dm.add_to_buffer(" ".join(
      [f"{self.color_dict[tile]}{tile}\033[0m" for tile in row]
      ))

  def print_stats(self, player: Player, last_user_input: str):
    p = player
    wood = p.inventory['wood']
    user_input = last_user_input.upper()
    self.dm.add_to_buffer("-" * os.get_terminal_size().columns)
    stats = f"Wood: {wood}, Hunger: {p.hunger}, Thirst: {p.thrist}, Last Input: {user_input}"
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
    args = text.split(", ") # Split the arguments with comma and space
    up = down = left = right = colors = "" 

    for arg in args:
      name = arg[0] # Name of the arg
      arg = arg[3:].strip() # Arg after the name, colon and space

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

    return [up, down, left, right, colors]

  def __getitem__(self, index: int):
    return self.game_map[index]

  def __len__(self):
    return len(self.game_map)


