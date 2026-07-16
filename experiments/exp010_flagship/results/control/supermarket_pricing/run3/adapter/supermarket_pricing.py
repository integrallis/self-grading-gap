# file: supermarket_pricing.py
from candidate import checkout as _checkout


class Checkout:
    def __init__(self):
        self._basket = list()

    def scan(self, item):
        self._basket.append(item)
        return self

    def scan_weighed(self, item, weight):
        self._basket.append(list((item, weight)))
        return self

    def total(self):
        return _checkout(self._basket)
