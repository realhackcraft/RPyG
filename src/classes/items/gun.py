from classes.items.item import Item


class Gun(Item):
    def __init__(self, quantity: int = 1) -> None:
        super().__init__(quantity)
