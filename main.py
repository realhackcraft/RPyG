import os
import random
import re
from copy import deepcopy

from classes.entity import Entity
from classes.player import Player
from utils.displayManager import DisplayManager

dm = DisplayManager()

def convert_arrow_keys(input_text):
  # Replace ANSI escape codes for arrow keys with corresponding WASD
  input_text = input_text.replace("\x1B[A", "W")
  input_text = input_text.replace("\x1B[B", "S")
  input_text = input_text.replace("\x1B[C", "D")
  input_text = input_text.replace("\x1B[D", "A")
  return input_text

def sanitize_ansi_escape(text):
  # Convert the arrow keys before they get removed
  text_without_arrow = convert_arrow_keys(text) 
  ansi_escape_pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
  # Replace ANSI escape codes with an empty string
  sanitized_text = ansi_escape_pattern.sub('', text_without_arrow)
  return sanitized_text

def parse_map_header(text):
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

def init(path):
  print("\033[=3h")  # Set display mode to 80x25 with color support
  game_map = []
  color_dict = {}

  with open(path, "r") as file:
    for i, line in enumerate(file):
      if i == 0:
        up, down, left, right, colors = parse_map_header(line)
        continue
      game_map.append(line.split())

    with open(colors, 'r') as color_file:
      for line in color_file:
        key, value = line.strip().split(' ')
        color_dict[key] = f"\033[{value}m"

  return [game_map, color_dict, up, down, left, right]

def display(game_map, display_map, player, entities):
  display_map = deepcopy(game_map)

  for e in entities:
    display_map[e.y][e.x] = e.symbol

  display_map[player.y][player.x] = player.symbol
  return display_map

def print_map(display_map, color_dict):
  for row in display_map:
    dm.add_to_buffer(" ".join(
      [f"{color_dict[tile]}{tile}\033[0m" for tile in row]
      ))

def split_string_with_capitals(s):
  return re.findall('[a-zA-Z][^A-Z]*', s)

def get_input():
  try:
    return sanitize_ansi_escape(input("> "))
  except KeyboardInterrupt:
    exit()

def clear_display():
  dm.add_to_buffer("\033[H\033[J")

def print_stats(player, last_user_input):
  p = player
  wood = p.inventory['wood']
  user_input = last_user_input.upper()
  dm.add_to_buffer("-" * os.get_terminal_size().columns)
  stats = f"Wood: {wood}, Hunger: {p.hunger}, Thirst: {p.thrist}, Last Input: {user_input}"
  dm.add_to_buffer(stats)
  dm.add_to_buffer("-" * os.get_terminal_size().columns)

def print_under(game_map, entities, player):
  dm.add_to_buffer("-" * os.get_terminal_size().columns)
  display_text = f"Block: {game_map[player.y][player.x]}, Entities: "
  for e in entities:
    if e.y == player.y and e.x == player.x:
      display_text += f"{e.name}, "
  dm.add_to_buffer(display_text.rstrip(", "))

def main():
  player = Player(2, 3)
  entities = []
  game_map, color_dict, up, down, left, right = init('./asset/map.txt')
  last_user_input = ""

  while True:
    display_map = display(game_map, [], player, entities)
    clear_display()

    print_under(game_map, entities, player)
    print_stats(player, last_user_input)
    print_map(display_map, color_dict)
    dm.flush_buffer()

    user_input = get_input()

    if user_input == "":
      user_input = last_user_input

    last_user_input = user_input

    commands = split_string_with_capitals(user_input)

    for c in commands:
      if c.lower() == "w":
        if player.y > 0:
         player.y -= 1
        elif up:
          game_map, color_dict, up, down, left, right = init(up) # Load upper map
          player.y = len(game_map) - 1
      elif c.lower() == "s":
        if player.y + 1 < len(game_map) - 1:
          player.y += 1
        elif down:
            game_map, color_dict, up, down, left, right = init(down)
            player.y = 0
      elif c.lower() == "a":
        if player.x > 0:
          player.x -= 1
        elif left:
          game_map, color_dict, up, down, left, right = init(left)
          player.x = 0
      elif c.lower() == "d":
        if player.x + 1 < len(game_map[player.y]):
          player.x += 1
        elif right:
          game_map, color_dict, up, down, left, right = init(right)
          player.x = len(game_map[player.y]) - 1
      elif c.lower() == "m":
        current_block = game_map[player.y][player.x]
        if current_block == "T" and player.hunger > 0 and player.thrist > 0:
          game_map[player.y][player.x] = "G"
          player.inventory['wood'] += 1
          player.hunger -= 1
          player.thrist -= 1
        elif current_block == "W":
          game_map[player.y][player.x] = "R"
          player.thrist += 1            
          if random.getrandbits(2) == 0:
            e = Entity("Salmon", "S", player.x, player.y, 1)
            entities.append(e)
      elif c.lower() == "e" and len(entities) > 0:
        for e in entities:
          if e.x == player.x and e.y == player.y:
            e.health -= 1
            if e.health <= 0:
              if e.name == "Salmon":
                player.hunger += 1
                entities.remove(e)

if __name__ == "__main__":
  main()
