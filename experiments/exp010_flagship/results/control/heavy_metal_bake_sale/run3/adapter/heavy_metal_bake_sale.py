# file: heavy_metal_bake_sale.py
from candidate import initialize_stock, quote_order_total, remaining_stock, take_payment


class NotEnoughMoneyError(Exception):
    pass


class OutOfStockError(Exception):
    pass


class BakeSale:
    def __init__(self, custom_stock=remaining_stock()):
        initialize_stock(custom_stock)

    def total(self, order):
        return quote_order_total(order)

    def pay(self, order, payment):
        return take_payment(order, payment)

    def stock_of(self, item):
        return remaining_stock().get(item)
