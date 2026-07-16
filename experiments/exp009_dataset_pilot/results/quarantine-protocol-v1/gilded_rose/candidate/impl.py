# candidate/impl.py

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return f"Item(name='{self.name}', sell_in={self.sell_in}, quality={self.quality})"


class InventoryManager:
    MAX_QUALITY = 50
    SULFURAS_NAME = "Sulfuras"
    AGED_BRIE_NAME = "Aged Brie"
    BACKSTAGE_PASS_NAME = "Backstage passes"
    CONJURED_NAME = "Conjured"

    def update_inventory(self, items: list[Item]):
        for item in items:
            self.update_item(item)

    def update_item(self, item: Item):
        if item.name == self.SULFURAS_NAME:
            return  # Sulfuras does not change

        item.sell_in -= 1

        if item.name == self.AGED_BRIE_NAME:
            self.update_aged_brie(item)
        elif item.name == self.BACKSTAGE_PASS_NAME:
            self.update_backstage_pass(item)
        elif item.name == self.CONJURED_NAME:
            self.update_conjured_item(item)
        else:
            self.update_regular_item(item)

    def update_regular_item(self, item: Item):
        degrade_amount = 1 if item.sell_in >= 0 else 2
        item.quality = max(0, item.quality - degrade_amount)

    def update_aged_brie(self, item: Item):
        increase_amount = 1 if item.sell_in >= 0 else 2
        item.quality = min(self.MAX_QUALITY, item.quality + increase_amount)

    def update_backstage_pass(self, item: Item):
        if item.sell_in < 0:
            item.quality = 0
        elif item.sell_in <= 5:
            item.quality = min(self.MAX_QUALITY, item.quality + 3)
        elif item.sell_in <= 10:
            item.quality = min(self.MAX_QUALITY, item.quality + 2)
        else:
            item.quality = min(self.MAX_QUALITY, item.quality + 1)

    def update_conjured_item(self, item: Item):
        degrade_amount = 4 if item.sell_in < 0 else 2
        item.quality = max(0, item.quality - degrade_amount)
