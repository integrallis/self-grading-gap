# file: supermarket_pricing.py
from decimal import Decimal

from candidate import checkout


class Checkout:
    def __init__(self):
        self.basket = []

    def scan(self, item):
        self.basket.append(item)

    def scan_weighed(self, fruit, weight):
        self.basket.append((fruit, weight))

    def total(self):
        return Decimal(str(checkout(self.basket)))
