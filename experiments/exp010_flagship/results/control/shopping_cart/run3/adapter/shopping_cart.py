# file: shopping_cart.py
from candidate import ShoppingCart as _CandidateShoppingCart


InsufficientStockError = ValueError
MaxQuantityExceededError = ValueError


class BulkPrice:
    def __init__(self, name, quantity_required, bulk_price):
        self.name = name
        self.quantity_required = quantity_required
        self.bulk_price = bulk_price

    def apply(self, cart):
        return cart._cart.apply_bulk_price_offer(
            self.name,
            self.quantity_required,
            self.bulk_price,
        )


BuyXGetYFree = BulkPrice


class PercentageDiscount:
    def __init__(self, percent):
        self.percent = percent

    def apply(self, cart):
        return cart._cart.apply_discount_percent(self.percent)


class FixedAmountDiscount:
    def __init__(self, amount):
        self.amount = amount

    def apply(self, cart):
        return cart._cart.apply_fixed_discount(self.amount)


class ShoppingCart:
    def __init__(self):
        self._cart = _CandidateShoppingCart()

    def add_item(self, *arguments):
        return self._cart.add_item(*arguments)

    def remove_item(self, name):
        return self._cart.remove_item(name)

    def update_quantity(self, name, quantity):
        return self._cart.change_quantity(name, quantity)

    def quantity_of(self, name):
        return self._cart.get_quantity(name)

    def item_subtotal(self, name):
        return self._cart.get_subtotal(name)

    def subtotal(self):
        return self._cart.get_pre_discount_sum()

    def total(self):
        return self._cart.get_total()

    def add_offer(self, offer):
        return offer.apply(self)

    def add_discount(self, discount):
        return discount.apply(self)
