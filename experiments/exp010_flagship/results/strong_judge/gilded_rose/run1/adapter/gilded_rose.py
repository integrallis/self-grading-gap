# file: gilded_rose.py
from candidate import update_inventory


AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes"
SULFURAS = "Sulfuras"
SULFURAS_QUALITY = int("80")


class Item(dict):
    def __init__(self, name, sell_in, quality):
        dict.__init__(
            self,
            name=name,
            days_remaining=sell_in,
            quality=quality,
        )

    @property
    def name(self):
        return self.get("name")

    @name.setter
    def name(self, value):
        self.update(name=value)

    @property
    def sell_in(self):
        return self.get("days_remaining")

    @sell_in.setter
    def sell_in(self, value):
        self.update(days_remaining=value)

    @property
    def days_remaining(self):
        return self.get("days_remaining")

    @days_remaining.setter
    def days_remaining(self, value):
        self.update(days_remaining=value)

    @property
    def quality(self):
        return self.get("quality")

    @quality.setter
    def quality(self, value):
        self.update(quality=value)


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        return update_inventory(self.items)
