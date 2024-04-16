class Structure:
  def __init__(self, path: str):
    self.path = path
    
    self.structure_map = []
    self.color_dict = {}
    
    with open(path, "r") as file:
      for i, line in enumerate(file):
        if i == 0:
          colors, structures, transparent = self.parse_structure_header(line)
          continue
        self.structure_map.append(line.split())

      with open(colors, 'r') as color_file:
        for line in color_file:
          key, value = line.strip().split(' ')
          self.color_dict[key] = f"\033[{value}m"
      
      self.transparent = transparent
      self.structures = structures
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
    colors = structures = transparent = "" 

    for arg in args:
      name = arg[0] # Name of the arg
      arg = arg[3:].strip() # Arg after the name, colon and space
      match name:
        case "C":
          colors = arg
        case "S":
          structures = arg.split(": ")
        case "T":
          transparent = arg

    return [colors, structures, transparent]

