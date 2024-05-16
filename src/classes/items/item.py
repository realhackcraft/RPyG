class Item:
    def __init__(self, quantity: int) -> None:
        self.name = type(self).__name__
        self.quantity = quantity

    def change_quantity(self, quantity: int):
        self.quantity += quantity
