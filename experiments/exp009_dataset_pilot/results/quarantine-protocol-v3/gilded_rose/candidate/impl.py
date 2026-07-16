# candidate/impl.py

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def update_quality(self):
        if self.name == "Sulfuras, Hand of Ragnaros":
            return  # Legendary item, no change
        
        if self.name == "Aged Brie":
            self._update_aged_brie()
        elif "Backstage passes" in self.name:
            self._update_backstage_pass()
        elif "Conjured" in self.name:
            self._update_conjured_item()
        else:
            self._update_regular_item()

        self.sell_in -= 1

    def _update_regular_item(self):
        if self.sell_in > 0:
            self.quality -= 1
        else:
            self.quality -= 2
        self.quality = max(0, self.quality)

    def _update_aged_brie(self):
        if self.sell_in > 0:
            self.quality += 1
        else:
            self.quality += 2
        self.quality = min(50, self.quality)

    def _update_backstage_pass(self):
        if self.sell_in > 10:
            self.quality += 1
        elif self.sell_in > 5:
            self.quality += 2
        elif self.sell_in > 0:
            self.quality += 3
        else:
            self.quality = 0
        
        self.quality = min(50, self.quality)

    def _update_conjured_item(self):
        if self.sell_in > 0:
            self.quality -= 2
        else:
            self.quality -= 4
        self.quality = max(0, self.quality)


class Inventory:
    def __init__(self, items: list):
        self.items = items

    def update_inventory(self):
        for item in self.items:
            item.update_quality()
