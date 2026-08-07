# file: supermarket_pricing.py
from candidate import checkout


class Checkout(list):
    def scan(self, item):
        list.append(self, item)

    def scan_weighed(self, name, weight):
        list.append(self, (name, weight))

    def total(self):
        return checkout(self)
