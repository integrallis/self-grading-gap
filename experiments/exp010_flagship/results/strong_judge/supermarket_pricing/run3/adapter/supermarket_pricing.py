# file: supermarket_pricing.py
from candidate import checkout as _checkout


class Checkout:
    def __init__(self):
        self._basket = list()

    def scan(self, item):
        _checkout((item,))
        self._basket.append(item)

    def scan_weighed(self, name, weight):
        _checkout(((name, weight),))
        self._basket.append((name, weight))

    def total(self):
        return _checkout(self._basket)
