# file: gilded_rose.py
from candidate.impl import GildedRose
from candidate.impl import Item

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"
SULFURAS_QUALITY = int("80")

GildedRose.update_quality = GildedRose.update_inventory
