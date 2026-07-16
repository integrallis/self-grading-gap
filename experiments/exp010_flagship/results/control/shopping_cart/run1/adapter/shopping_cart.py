# file: shopping_cart.py
from candidate import ShoppingCart as _CandidateShoppingCart


InsufficientStockError = ValueError
MaxQuantityExceededError = ValueError


class BulkPrice:
    def __init__(self, name, min_quantity, bulk_price):
        self.name = name
        self.min_quantity = min_quantity
        self.bulk_price = bulk_price

    def add_to(self, cart):
        return cart._add_bulk_offer(
            self.name,
            self.min_quantity,
            self.bulk_price,
        )


class BuyXGetYFree:
    def __init__(self, name, buy, get):
        self.name = name
        self.buy = buy
        self.get = get

    def add_to(self, cart):
        return cart._add_buy_x_get_y_offer(
            self.name,
            self.buy,
            self.get,
        )


class PercentageDiscount:
    def __init__(self, percent):
        self.percent = percent

    def add_to(self, cart):
        return cart.apply_percentage_discount(self.percent)


class FixedAmountDiscount:
    def __init__(self, amount):
        self.amount = amount

    def add_to(self, cart):
        return cart.apply_fixed_amount_discount(self.amount)


class ShoppingCart(_CandidateShoppingCart):
    subtotal = _CandidateShoppingCart.get_total
    total = _CandidateShoppingCart.get_total
    item_subtotal = _CandidateShoppingCart.get_subtotal
    quantity_of = _CandidateShoppingCart.get_quantity
    update_quantity = _CandidateShoppingCart.change_quantity

    def add_discount(self, discount):
        return discount.add_to(self)

    def add_offer(self, offer):
        return offer.add_to(self)

    def _add_bulk_offer(self, name, min_quantity, bulk_price):
        return _CandidateShoppingCart.add_offer(
            self,
            name,
            min_quantity=min_quantity,
            bulk_price=bulk_price,
        )

    def _add_buy_x_get_y_offer(self, name, buy, get):
        return _CandidateShoppingCart.add_offer(
            self,
            name,
            buy=buy,
            get=get,
        )
