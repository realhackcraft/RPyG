from classes.items.item import Item
from main import Main


class Gun(Item):
    def __init__(self, quantity: int = 1) -> None:
        super().__init__(quantity)

    def use(self) -> None:
        direction = Main.commands[Main.current_command_index + 1]
        match direction.lower():
            case "w":
                pass
            case "a":
                pass
            case "s":
                pass
            case "d":
                pass
            case _:
                self.use()
