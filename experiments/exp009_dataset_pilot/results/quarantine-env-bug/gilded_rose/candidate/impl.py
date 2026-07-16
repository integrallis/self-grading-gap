# candidate/impl.py

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def update(self):
        raise NotImplementedError("This method should be overridden in subclasses.")

class RegularItem(Item):
    def update(self):
        self.sell_in -= 1
        if self.sell_in < 0:
            self.quality = max(0, self.quality - 2)
        else:
            self.quality = max(0, self.quality - 1)

class AgedBrie(Item):
    def update(self):
        self.sell_in -= 1
        if self.sell_in < 0:
            self.quality = min(50, self.quality + 2)
        else:
            self.quality = min(50, self.quality + 1)

class Sulfuras(Item):
    def update(self):
        pass  # Sulfuras does not change

class BackstagePass(Item):
    def update(self):
        self.sell_in -= 1
        if self.sell_in < 0:
            self.quality = 0
        elif self.sell_in < 6:
            self.quality = min(50, self.quality + 3)
        elif self.sell_in < 11:
            self.quality = min(50, self.quality + 2)
        else:
            self.quality = min(50, self.quality + 1)

class ConjuredItem(Item):
    def update(self):
        self.sell_in -= 1
        if self.sell_in < 0:
            self.quality = max(0, self.quality - 4)
        else:
            self.quality = max(0, self.quality - 2)

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item: Item):
        self.items.append(item)

    def update_inventory(self):
        for item in self.items:
            item.update()
