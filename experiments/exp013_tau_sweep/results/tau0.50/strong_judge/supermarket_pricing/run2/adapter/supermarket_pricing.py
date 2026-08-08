# file: supermarket_pricing.py
from candidate import checkout


class Checkout:
    def __init__(self):
        self.basket = []

    def scan(self, item):
        self.basket.append(item)

    def scan_weighed(self, name, weight):
        self.basket.append((name, weight))

    def total(self):
        return checkout(self.basket)
