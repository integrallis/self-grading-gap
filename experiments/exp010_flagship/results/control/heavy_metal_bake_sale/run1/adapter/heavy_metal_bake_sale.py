# file: heavy_metal_bake_sale.py
from candidate import StockError
from candidate import quote_order
from candidate import remaining_stock
from candidate import take_payment

NotEnoughMoneyError = StockError
OutOfStockError = StockError


class BakeSale:
    def __init__(self, *args):
        pass

    def total(self, order):
        return quote_order(order)

    def stock_of(self, item):
        return remaining_stock().get(item)

    def pay(self, order, amount):
        return take_payment(amount)
