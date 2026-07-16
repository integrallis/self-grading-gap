# candidate/impl.py

from gilded_rose import AGED_BRIE
from gilded_rose import BACKSTAGE_PASS
from gilded_rose import GildedRose, Item
from gilded_rose import SULFURAS
from gilded_rose import SULFURAS_QUALITY

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def update_quality(self):
        if self.name == SULFURAS:
            return
        
        self.sell_in -= 1
        
        if self.name == AGED_BRIE:
            self._update_aged_brie()
        elif self.name == BACKSTAGE_PASS:
            self._update_backstage_passes()
        elif "Conjured" in self.name:
            self._update_conjured()
        else:
            self._update_regular()

    def _update_regular(self):
        decrease = 2 if self.sell_in < 0 else 1
        self.quality = max(0, self.quality - decrease)

    def _update_aged_brie(self):
        increase = 2 if self.sell_in < 0 else 1
        self.quality = min(50, self.quality + increase)

    def _update_backstage_passes(self):
        if self.sell_in < 0:
            self.quality = 0
        elif self.sell_in < 6:
            self.quality = min(50, self.quality + 3)
        elif self.sell_in < 11:
            self.quality = min(50, self.quality + 2)
        else:
            self.quality = min(50, self.quality + 1)

    def _update_conjured(self):
        decrease = 4 if self.sell_in < 0 else 2
        self.quality = max(0, self.quality - decrease)


class GildedRose:
    def __init__(self, items: list[Item]):
        self.items = items

    def update_inventory(self):
        for item in self.items:
            item.update_quality()
