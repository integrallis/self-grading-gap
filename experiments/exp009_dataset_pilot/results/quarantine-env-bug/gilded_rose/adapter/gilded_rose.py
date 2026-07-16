# file: gilded_rose.py

from candidate.impl import GildedRose as _GildedRose
from candidate.impl import Item as _Item

class GildedRose:
    def __init__(self, items):
        self.gilded_rose = _GildedRose(items)

    def update_inventory(self):
        self.gilded_rose.update_inventory()

class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self._item = _Item(name, sell_in, quality)

    @property
    def name(self):
        return self._item.name

    @property
    def sell_in(self):
        return self._item.sell_in

    @property
    def quality(self):
        return self._item.quality

    def update(self):
        self._item.update()
