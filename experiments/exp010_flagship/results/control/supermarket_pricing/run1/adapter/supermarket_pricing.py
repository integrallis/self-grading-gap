# file: supermarket_pricing.py
from decimal import Decimal
from candidate import checkout


class Checkout:
    def __init__(self):
        self._items = list()

    def scan(self, item):
        pending = list(self._items)
        pending.append(item)
        checkout(pending)
        return self._items.append(item)

    def scan_weighed(self, item, weight):
        pending = list(self._items)
        pending.append((item, float(weight)))
        checkout(pending)
        return self._items.append((item, float(weight)))

    def total(self):
        return Decimal(str(checkout(self._items)))
