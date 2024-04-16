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
        with open(colors, 'r') as color_file:
          for line in color_file:
            key, value = line.strip().split(' ')
            self.color_dict[key] = f"\033[{value}m"
      
      self.transparent = transparent
      self.structures = structures
      self.symbol = symbol

      self.loaded_structures = []

      if self.structures:
        for structure in self.structures:
          self.loaded_structures.append(Structure(structure))

      # Replace the transparent tiles with space
      for row in self.structure_map:
        for tile in row:
          if tile == self.transparent:
            tile = " "


  @staticmethod
  def parse_structure_header(text: str):
    args = text.split(", ") # Split the arguments with comma and space
    colors = structures = transparent = symbol = "" 

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

    return [colors, structures, transparent, symbol]


