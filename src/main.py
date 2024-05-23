import random
import re
import sys

from classes.entities.bear import Bear
from classes.entities.entity import Entity
from classes.entities.player import Player
from classes.enums.mode import Mode
from classes.items.wood import Wood
from classes.map import Map
from utils.display_manager import DisplayManager
from utils.string import StringUtils

display_manager = DisplayManager()


class Main:
    def __init__(self) -> None:
        self.main()
        Main.commands = []
        Main.current_command = ""
        Main.current_command_index = 0

    def convert_arrow_keys(self, input_text: str):
        # Replace ANSI escape codes for arrow keys with corresponding WASD
        input_text = input_text.replace("\x1B[A", "W")
        input_text = input_text.replace("\x1B[B", "S")
        input_text = input_text.replace("\x1B[C", "D")
        input_text = input_text.replace("\x1B[D", "A")
        return input_text

    def sanitize_ansi_escape(self, text: str):
        # Convert the arrow keys before they get removed
        text_without_arrow = self.convert_arrow_keys(text)
        ansi_escape_pattern = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        # Replace ANSI escape codes with an empty string
        sanitized_text = ansi_escape_pattern.sub("", text_without_arrow)
        return sanitized_text

    def main(self):
        player = Player(2, 3)
        game_map = Map("./assets/map.txt", display_manager)
        last_user_input = ""

        ### TEST ###
        game_map.entities.append(Bear(10, 10))
        ### END TEST ###

        print("\033[=3h")  # Set display mode to 80x25 with color support

        mode = Mode.NORMAL
        inventory_mode_selected_item_index = 0
        item = None

        while True:
            display_manager.clear_display()
            game_map.render_map(player, game_map.entities, last_user_input)
            display_manager.flush_buffer()

            user_input = ""

            try:
                if mode == Mode.NORMAL:
                    user_input = self.sanitize_ansi_escape(input("> "))
                elif mode == Mode.INVENTORY:
                    item = player.inventory[inventory_mode_selected_item_index]
                    user_input = self.sanitize_ansi_escape(
                        input(f"{item.name} - {item.quantity} > ")
                    )
            except KeyboardInterrupt:
                sys.exit()

            if user_input == "":
                user_input = last_user_input

            last_user_input = user_input

            Main.commands = StringUtils.split_string_with_capitals(user_input)

            for i, j in enumerate(Main.commands):
                c = Main.current_command
                Main.current_command = j
                Main.current_command_index = i
                if mode == Mode.NORMAL:
                    for e in game_map.entities:
                        if isinstance(e, Bear):
                            e.tick(player, game_map)
                        else:
                            e.tick()

                    match c.lower():
                        case "w":
                            if player.y > 0:
                                player.y -= 1
                            elif game_map.loaded_up:
                                # This is ducplicated and not referenced
                                temp_game_map = game_map
                                game_map = game_map.loaded_up  # Load upper map
                                # Only load the surrounding maps once it exists

                                game_map.load_path()
                                game_map.loaded_down = (
                                    temp_game_map  # This is the old game_map
                                )

                                player.y = len(game_map) - 1
                                player.x = min(
                                    len(game_map[player.y]) - 1, player.x
                                )  # Make sure player.x is in bounds
                        case "s":
                            if player.y + 1 < len(game_map):
                                player.y += 1
                            elif game_map.loaded_down:
                                temp_game_map = game_map
                                game_map = game_map.loaded_down
                                game_map.load_path()
                                game_map.loaded_up = temp_game_map

                                player.y = 0
                                player.x = min(
                                    len(game_map[player.y]) - 1, player.x
                                )  # Make sure player.x is in bounds
                        case "a":
                            if player.x > 0:
                                player.x -= 1
                            elif game_map.loaded_left:
                                temp_game_map = game_map
                                game_map = game_map.loaded_left
                                game_map.load_path()
                                game_map.loaded_right = temp_game_map

                                player.x = 0
                                player.y = min(
                                    len(game_map) - 1, player.y
                                )  # Make sure player.y is in bouds
                        case "d":
                            if player.x + 1 < len(game_map[player.y]):
                                player.x += 1
                            elif game_map.loaded_right:
                                temp_game_map = game_map
                                game_map = game_map.loaded_right
                                game_map.load_path()
                                game_map.loaded_left = temp_game_map

                                player.x = len(game_map[player.y]) - 1
                                player.y = min(
                                    len(game_map) - 1, player.y
                                )  # Make sure player.y is in bouds
                        case "m":
                            current_block = game_map[player.y][player.x]
                            if (
                                current_block == "T"
                                and player.hunger > 0
                                and player.thirst > 0
                            ):
                                game_map[player.y][player.x] = "G"
                                player.inventory.add_item(Wood())
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
                                        if e.health > 0:
                                            return
                                        match e.name:
                                            case "Salmon":
                                                if player.set_hunger(player.hunger + 1):
                                                    game_map.entities.remove(e)
                        case "i":
                            mode = Mode.INVENTORY
                elif mode == Mode.INVENTORY:
                    match c.lower():
                        case "w":
                            if inventory_mode_selected_item_index - 1 >= 0:
                                inventory_mode_selected_item_index -= 1
                            else:
                                # Wrap around the inventory of it is exeeded
                                inventory_mode_selected_item_index = (
                                    len(player.inventory) - 1
                                )
                        case "s":
                            if inventory_mode_selected_item_index + 1 < len(
                                player.inventory
                            ):
                                inventory_mode_selected_item_index += 1
                            else:
                                inventory_mode_selected_item_index = 0
                        case "u":
                            if item is None:
                                raise TypeError()
                            item.use()
                        case "q":
                            mode = Mode.NORMAL


if __name__ == "__main__":
    Main()
