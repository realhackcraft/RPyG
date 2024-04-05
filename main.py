import os
import random
import re
import sys
from copy import deepcopy

from classes.entity import Entity
from classes.player import Player


def parse_map_header(line):
  args = line.split(", ") # Split the arguments with comma and space
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
  print("\033[=3h") # Set display mode to 80x25 with color support
  game_map = []
  color_dict = {}

  up = down = left = right = colors = "" 

  with open(path, "r") as file:
    lines = 0
    for i, line in enumerate(file):
      if lines == 0:
         up, down, left, right, colors = parse_map_header(line)
         lines += 1 # Make sure the line gets incresed because the other lines += 1 code doesn't get run when lines == 1
         continue

      game_map.append(line.split())
      lines += 1
    print(colors)
    with open(colors, 'r') as file:
      for line in file:
        # Split each line into key and value based on space
        key, value = line.strip().split(' ')
        # Add key-value pair to the dictionarycolor_dict
        color_dict[key] = f"\033[{value}m"
  return [game_map, color_dict]

def display(game_map, display_map, player, entities):
  display_map = deepcopy(game_map)

  for e in entities:
    display_map[e.y][e.x] = e.symbol
  
  display_map[player.y][player.x] = player.symbol
  return display_map

def print_map(display_map, color_dict):
  for row in display_map:
    for tile in row:
      print(color_dict[tile] + tile + "\033[0m", end=" ")  # get color of tile
    print()  # new line

def split_string_with_capitals(s):
    return re.findall('[a-zA-Z][^A-Z]*', s)

def get_input():
  try:
    return input("> ")
  except KeyboardInterrupt:
    # handle ^C gracefully
    exit()

def clear_display():
  for _ in range(os.get_terminal_size().columns): # Clear up the entire screen
    sys.stdout.write("\033[F")  # Move cursor up one line
    sys.stdout.write("\033[K")  # Clear to the end of line

def print_stats(player, last_user_input):
  print("-"*os.get_terminal_size().columns)
  print(f"Wood: {player.inventory['wood']}, Hunger: {player.hunger}, Thirst: {player.thrist}, Last Input: {last_user_input.upper()}")
  print("-"*os.get_terminal_size().columns)


def print_under(game_map, entities, player):
  print("-"*os.get_terminal_size().columns)

  display_text = f"Block: {game_map[player.y][player.x]}, Entities: "
  
  for e in entities:
    first = True
    if e.y == player.y and e.x == player.x:
      if first:
        display_text += f"{e.name}"
        first = False
      else:
        display_text += f", {e.name}"
  print(display_text)


def main():

  player = Player(2, 3)

  entities = []

  game_map = []
  display_map = []

  color_dict = {}

  last_user_input = ""
  
  game_map, color_dict = init('./map.txt')
  
  while True:
    display_map = display(game_map, display_map, player, entities)
    clear_display()

    print_under(game_map, entities, player) # shows what's under the player
    print_stats(player, last_user_input)
    print_map(display_map, color_dict)
    
    user_input = get_input()

    if user_input == "":
      user_input = last_user_input # repeat last user input if the user presses enter
    
    last_user_input = user_input

    commands = split_string_with_capitals(user_input)

    for c in commands:
      match c.lower():
        case "w":
          if player.y > 0:
            player.y -= 1
        case "s":
          if player.y + 1 < len(game_map) - 1: # The length of an array is it's max available index + 1
            player.y += 1
        case "a":
          if player.x > 0:
            player.x -= 1
        case "d":
          if player.x + 1 < len(game_map[player.y]):
            player.x += 1
        case "m":
          current_block = game_map[player.y][player.x]
          if current_block == "T":
            if player.hunger > 0 and player.thrist > 0:
              game_map[player.y][player.x] = "G" # mine the tree
              player.inventory['wood'] += 1
              player.hunger -= 1
              player.thrist -= 1
          elif current_block == "W":
            game_map[player.y][player.x] = "R" # drink the water
            player.thrist += 1
            if random.getrandbits(2) == 0: # 1/4
              e = Entity("Salmon", "S", player.x, player.y, 1)
              entities.append(e)
        case "e":
          # check if salmon is on the same positiion as the player
          if len(entities) > 0:
            for e in entities:
              if e.x == player.x and e.y == player.y:
                e.health -= 1
                if e.health <= 0:
                  match e.name:
                    case "Salmon":
                      player.hunger += 1
                  entities.remove(e)

if __name__ == "__main__":
  main()

