# file: gilded_rose.py
from candidate import update_inventory as _update_inventory


AGED_BRIE = "Aged Brie"
SULFURAS = "Sulfuras"
BACKSTAGE_PASS = "Backstage Pass"
SULFURAS_QUALITY = int("80")


class Item:
    def __init__(self, name, sell_in, quality):
        self._record = dict(
            name=name,
            days_remaining=sell_in,
            quality=quality,
        )

    @property
    def name(self):
        return self._record.get("name")

    @name.setter
    def name(self, value):
        self._record.update(name=value)

    @property
    def sell_in(self):
        return self._record.get("days_remaining")

    @sell_in.setter
    def sell_in(self, value):
        self._record.update(days_remaining=value)

    @property
    def quality(self):
        return self._record.get("quality")

    @quality.setter
    def quality(self, value):
        self._record.update(quality=value)

    def __repr__(self):
        return "{}, {}, {}".format(self.name, self.sell_in, self.quality)


def _record_for(item):
    return item._record


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        return _update_inventory(list(map(_record_for, self.items)))
