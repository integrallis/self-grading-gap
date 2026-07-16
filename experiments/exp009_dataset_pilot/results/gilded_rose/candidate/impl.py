# candidate/impl.py

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def update(self):
        if self.name == "Sulfuras, Hand of Ragnaros":
            return  # Sulfuras never changes

        self.sell_in -= 1

        if self.name == "Aged Brie":
            self._update_aged_brie()
        elif self.name == "Backstage passes to a TAFKAL80ETC concert":
            self._update_backstage_pass()
        elif "Conjured" in self.name:
            self._update_conjured()
        else:
            self._update_regular()

    def _update_regular(self):
        self._change_quality(-1)

        if self.sell_in < 0:
            self._change_quality(-1)

    def _update_aged_brie(self):
        self._change_quality(1)

        if self.sell_in < 0:
            self._change_quality(1)

    def _update_backstage_pass(self):
        if self.sell_in > 10:
            self._change_quality(1)
        elif self.sell_in > 5:
            self._change_quality(2)
        elif self.sell_in > 0:
            self._change_quality(3)
        else:
            self.quality = 0

    def _update_conjured(self):
        self._change_quality(-2)

        if self.sell_in < 0:
            self._change_quality(-2)

    def _change_quality(self, amount):
        self.quality += amount
        if self.quality < 0:
            self.quality = 0
        if self.quality > 50:
            self.quality = 50


class GildedRose:
    def __init__(self, items):
        self.items = items

    def update_inventory(self):
        for item in self.items:
            item.update()
