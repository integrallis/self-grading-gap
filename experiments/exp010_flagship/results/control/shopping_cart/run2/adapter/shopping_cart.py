# file: shopping_cart.py
from candidate import ShoppingCart as _ShoppingCart

InsufficientStockError = ValueError
MaxQuantityExceededError = ValueError


class BulkPrice:
    def __init__(self, name, minimum_quantity, price):
        self.name = name
        self.minimum_quantity = minimum_quantity
        self.price = price

    def apply(self, cart):
        return cart.apply_bulk_price_offer(
            self.name,
            self.minimum_quantity,
            self.price,
        )


class BuyXGetYFree:
    def __init__(self, name, buy, get):
        self.name = name
        self.buy = buy
        self.get = get

    def apply(self, cart):
        return cart.apply_offer(self.name, self.buy, self.get)


class PercentageDiscount:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, cart):
        return cart.apply_discount(self.percent)


class FixedAmountDiscount:
    def __init__(self, amount):
        self.amount = amount

    def apply(self, cart):
        return cart.apply_fixed_discount(self.amount)


class ShoppingCart:
    def __init__(self):
        self._cart = _ShoppingCart()

    def add_item(self, *args):
        return self._cart.add_item(*args)

    def remove_item(self, name):
        return self._cart.remove_item(name)

    def update_quantity(self, *args):
        return self._cart.change_quantity(*args)

    def quantity_of(self, name):
        return self._cart.get_quantity(name)

    def item_subtotal(self, name):
        return self._cart.get_subtotal(name)

    def subtotal(self):
        return self._cart.get_pre_discount_sum()

    def total(self):
        return self._cart.get_total()

    def add_offer(self, offer):
        return offer.apply(self._cart)

    def add_discount(self, discount):
        return discount.apply(self._cart)
