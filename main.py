import random
import re

from classes.entity import Entity
from classes.player import Player
from classes.map import Map
from utils.displayManager import DisplayManager
from utils.string import StringUtils

dm = DisplayManager()

def convert_arrow_keys(input_text: str):
  # Replace ANSI escape codes for arrow keys with corresponding WASD
  input_text = input_text.replace("\x1B[A", "W")
  input_text = input_text.replace("\x1B[B", "S")
  input_text = input_text.replace("\x1B[C", "D")
  input_text = input_text.replace("\x1B[D", "A")
  return input_text

def sanitize_ansi_escape(text: str):
  # Convert the arrow keys before they get removed
  text_without_arrow = convert_arrow_keys(text) 
  ansi_escape_pattern = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
  # Replace ANSI escape codes with an empty string
  sanitized_text = ansi_escape_pattern.sub('', text_without_arrow)
  return sanitized_text

def get_input():
  try:
    return sanitize_ansi_escape(input("> "))
  except KeyboardInterrupt:
    exit()

def clear_display():
  dm.add_to_buffer("\033[H\033[J")

def main():
  player = Player(2, 3)
  entities = []
  game_map = Map("./assets/map.txt", dm)
  last_user_input = ""

  print("\033[=3h")  # Set display mode to 80x25 with color support

  while True:
    clear_display()
    game_map.render_map(player, entities, last_user_input)
    dm.flush_buffer()

    user_input = get_input()

    if user_input == "":
      user_input = last_user_input

    last_user_input = user_input

    commands = StringUtils.split_string_with_capitals(user_input)

    for c in commands:
      match c.lower():
        case "w":
          if player.y > 0:
            player.y -= 1
          elif game_map.up:
            game_map = Map(game_map.up, dm) # Load upper map
            player.y = len(game_map) - 1
            player.x = min(len(game_map[player.y]) - 1, player.x) # Make sure player.x is in bounds
        case "s":
          if player.y + 1 < len(game_map) :
            player.y += 1
          elif game_map.down:
            game_map = Map(game_map.down, dm)
            player.y = 0
            player.x = min(len(game_map[player.y]) , player.x) # Make sure player.x is in bounds
        case "a":
          if player.x > 0:
            player.x -= 1
          elif game_map.left:
            game_map = Map(game_map.left, dm)
            player.x = 0
            player.y = min(len(game_map) - 1, player.y) # Make sure player.y is in bouds
        case "d":
          if player.x + 1 < len(game_map[player.y]):
            player.x += 1
          elif game_map.right:
            game_map = Map(game_map.right, dm)
            player.x = len(game_map[player.y]) - 1
            player.y = min(len(game_map) - 1, player.y) # Make sure player.y is in bouds
        case "m":
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
        case "e":
          if len(entities) > 0:
            for e in entities:
              if e.x == player.x and e.y == player.y:
                e.health -= 1
                if e.health <= 0:
                  if e.name == "Salmon":
                    player.hunger += 1
                    entities.remove(e)

if __name__ == "__main__":
  main()

