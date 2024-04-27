"""
Classes for structures that are overlayed on top of maps
"""

from typing import List, Tuple

from utils.file import FileUtils

class Structure:
  def __init__(self, path: str):
    self.path = path
    
    self.structure_map = []
    self.color_dict = {}

    colors = structures = transparent = symbol = None


    with open(self.path, "r") as file:
      for i, line in enumerate(file):
        if i == 0:
          colors, structures, transparent, symbol = self.parse_structure_header(line)
          continue
        self.structure_map.append(line.split())
     
      if colors:
        self.color_dict = FileUtils.parse_colors(colors)

      self.transparent = transparent
      self.structures = structures
      self.symbol = symbol

      self.loaded_structures: List[Structure] = []

      if self.structures:
        for structure in self.structures:
          self.loaded_structures.append(Structure(structure))

      # Replace the transparent tiles with empty space
      for row in self.structure_map:
        for tile in row:
          if tile == self.transparent:
            tile = " "

  def render_structure(self, map_size: Tuple[int], rendered_map: List[List]=[[]]) -> List[List[str]]:
    # add the structure_map to the rendered map
    
    for s in self.loaded_structures:
      rendered_map = s.render_structure(map_size, rendered_map)
    
    return rendered_map 
    
  @staticmethod
  def parse_structure_header(text: str) -> Tuple[str, List[str], str, str]:
    args = text.split(", ") # Split the arguments with comma and space
    colors = transparent = symbol = "" 
    structures = []

    for arg in args:
      name = arg[0] # Name of the arg
      arg = arg[3:].strip() # Arg after the name, colon and space
      match name:
        case "C":
          colors = arg
        case "I":
          structures = arg.split("; ")
        case "T":
          transparent = arg
        case "S":
          symbol = arg

    return (colors, structures, transparent, symbol)


