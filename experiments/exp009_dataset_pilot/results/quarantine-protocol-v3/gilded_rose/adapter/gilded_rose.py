# file: gilded_rose.py
from candidate.impl import Inventory
from candidate.impl import Item

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
SULFURAS_QUALITY = int("80")


class GildedRose(Inventory):
    update_quality = Inventory.update_inventory
