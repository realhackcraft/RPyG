import random
import re

from classes.bear import Bear
from classes.entity import Entity
from classes.player import Player
from classes.map import Map, deepcopy
from utils.displayManager import DisplayManager
from utils.string import StringUtils

display_manager = DisplayManager()

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

def clear_display():
  display_manager.add_to_buffer("\033[H\033[J")

def main():
  player = Player(2, 3)
  game_map = Map("./assets/map.txt", display_manager)
  last_user_input = ""
  
  ### TEST ###
  game_map.entities.append(Bear(10, 10))
  ### END TEST ###

  print("\033[=3h")  # Set display mode to 80x25 with color support

  mode = "NORMAL"

  while True:

    inventory_mode_selected_item_index = 0
    clear_display()
    game_map.render_map(player, game_map.entities, last_user_input)
    display_manager.flush_buffer()


    user_input = ""

    try:
      if mode == "NORMAL":
        user_input = sanitize_ansi_escape(input("> "))
      elif mode == "INVENTORY":
        item = list(player.inventory.items())[inventory_mode_selected_item_index]
        user_input = sanitize_ansi_escape(input(f"{item[0]} - {item[1]} > "))
    except KeyboardInterrupt:
      exit()

    if user_input == "":
      user_input = last_user_input

    last_user_input = user_input

    commands = StringUtils.split_string_with_capitals(user_input)

    for c in commands:
      if mode == "NORMAL":
        for e in game_map.entities:
          if type(e) is Bear:
            e.tick(player, game_map)
          else:
            e.tick()

        match c.lower():
          case "w":
            if player.y > 0:
              player.y -= 1
            elif game_map.loaded_up:
              temp_game_map = game_map # This is ducplicated and not referenced
              game_map = game_map.loaded_up # Load upper map
              game_map.load_path() # Only load the surrounding maps once it is loaded
              game_map.loaded_down = temp_game_map # This is the old game_map

              player.y = len(game_map) - 1
              player.x = min(len(game_map[player.y]) - 1, player.x) # Make sure player.x is in bounds
          case "s":
            if player.y + 1 < len(game_map):
              player.y += 1
            elif game_map.loaded_down:
              temp_game_map = game_map
              game_map = game_map.loaded_down
              game_map.load_path()
              game_map.loaded_up = temp_game_map

              player.y = 0
              player.x = min(len(game_map[player.y]) - 1, player.x) # Make sure player.x is in bounds
          case "a":
            if player.x > 0:
              player.x -= 1
            elif game_map.left:
              temp_game_map = game_map
              game_map = game_map.loaded_left
              game_map.load_path()
              game_map.loaded_right = temp_game_map

              player.x = 0
              player.y = min(len(game_map) - 1, player.y) # Make sure player.y is in bouds
          case "d":
            if player.x + 1 < len(game_map[player.y]):
              player.x += 1
            elif game_map.right:
              temp_game_map = game_map
              game_map = game_map.loaded_right
              game_map.load_path()
              game_map.loaded_left = temp_game_map

              player.x = len(game_map[player.y]) - 1
              player.y = min(len(game_map) - 1, player.y) # Make sure player.y is in bouds
          case "m":
            current_block = game_map[player.y][player.x]
            if current_block == "T" and player.hunger > 0 and player.thirst > 0:
              game_map[player.y][player.x] = "G"
              player.inventory['wood'] += 1
              player.set_hunger(player.hunger - 1)
              player.set_thirst(player.thirst - 1)
            elif current_block == "W":
              if player.set_thirst(player.thirst + 1):
                game_map[player.y][player.x] = "R"
                if random.getrandbits(2) == 0:
                  e = Entity("Salmon", "S", player.x, player.y, 1)
                  game_map.entities.append(e)
          case "e":
            if len(game_map.entities) > 0:
              for e in game_map.entities:
                if e.x == player.x and e.y == player.y:
                  e.health -= 1
                  if e.health <= 0:
                    if e.name == "Salmon":
                      if player.set_hunger(player.hunger + 1):
                        game_map.entities.remove(e)
          case "i":
            mode = "INVENTORY"
      elif mode == "INVENTORY":
        match c.lower():
          case "w":
            if inventory_mode_selected_item_index - 1 >= 0:
              inventory_mode_selected_item_index -= 1
          case "s":
            if inventory_mode_selected_item_index + 1 > len(player.inventory):
              inventory_mode_selected_item_index += 1
          case "q":
            mode = "NORMAL"

if __name__ == "__main__":
  main()

