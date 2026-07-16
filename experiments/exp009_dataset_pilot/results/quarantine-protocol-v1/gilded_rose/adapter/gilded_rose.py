# file: gilded_rose.py

from candidate.impl import InventoryManager as _InventoryManager
from candidate.impl import Item as _Item

AGED_BRIE = _InventoryManager.AGED_BRIE_NAME
SULFURAS = _InventoryManager.SULFURAS_NAME
BACKSTAGE_PASS = _InventoryManager.BACKSTAGE_PASS_NAME

class GildedRose:
    def __init__(self, items: list[_Item]):
        self.items = items
        self.manager = _InventoryManager()

    def update_quality(self):
        self.manager.update_inventory(self.items)

class Item(_Item):
    pass
