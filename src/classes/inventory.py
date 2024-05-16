from classes.items.item import Item

class Inventory:
    def __init__(self) -> None:
        self.__items__ = []


    def has_item(self, item: Item) -> Item | None:
        for i in self.__items__:
            if type(i) is type(item):
                return i
        return None


    def add_item(self, item: Item) -> None:
        self_item = self.has_item(item)
        if self_item is None:
            self.__items__.append(item)
        else:
            quantity = item.quantity
            self_item.change_quantity(quantity)
       

    def remove_item(self, item: Item) -> bool:
        self_item = self.has_item(item)
        if self_item is None:
            return False
        
        quantity = item.quantity
        self_item.change_quantity(-quantity)
        return True



    def __len__(self) -> int:
        return len(self.__items__)

    def __getitem__(self, i: int) -> Item:
        return self.__items__[i]

