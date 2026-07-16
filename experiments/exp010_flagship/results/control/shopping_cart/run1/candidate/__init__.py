class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.discount = 0.0

    def add_item(self, name, unit_price, quantity=1, stock=None, max_quantity=None, discountable=True):
        if not name:
            raise ValueError("item name must not be empty")
        if unit_price < 0:
            raise ValueError(f"unit_price must be non-negative, got {unit_price}")
        if quantity < 1:
            raise ValueError(f"quantity must be at least 1, got {quantity}")
        if stock is not None and stock < 0:
            raise ValueError(f"stock must be non-negative, got {stock}")
        if max_quantity is not None and max_quantity < 1:
            raise ValueError(f"max_quantity must be at least 1, got {max_quantity}")
        if stock is not None and quantity > stock:
            raise ValueError(f"only {stock} of {name} in stock, requested {quantity}")

        if name in self.items:
            current_quantity = self.items[name]['quantity']
            if max_quantity is not None and current_quantity + quantity > max_quantity:
                raise ValueError(f"maximum {max_quantity} of {name} per order, requested {current_quantity + quantity}")
            self.items[name]['quantity'] += quantity
        else:
            if max_quantity is not None and quantity > max_quantity:
                raise ValueError(f"maximum {max_quantity} of {name} per order, requested {quantity}")
            self.items[name] = {'unit_price': unit_price, 'quantity': quantity, 'discountable': discountable}

    def remove_item(self, name):
        if name not in self.items:
            raise ValueError(f"item {name} is not in the cart")
        del self.items[name]

    def change_quantity(self, name, new_quantity):
        if name not in self.items:
            raise ValueError(f"item {name} is not in the cart")
        if new_quantity < 0:
            raise ValueError(f"quantity must be non-negative, got {new_quantity}")
        if new_quantity == 0:
            self.remove_item(name)
        else:
            self.items[name]['quantity'] = new_quantity

    def get_quantity(self, name):
        return self.items.get(name, {'quantity': 0})['quantity']

    def get_subtotal(self, name):
        if name not in self.items:
            raise ValueError(f"item {name} is not in the cart")
        item = self.items[name]
        return item['unit_price'] * item['quantity'] * (1 - (self.discount if item['discountable'] else 0))

    def get_total(self):
        return sum(self.get_subtotal(name) for name in self.items)

    def apply_percentage_discount(self, percent):
        if not (0 < percent <= 100):
            raise ValueError(f"percent must be greater than 0 and at most 100, got {percent}")
        self.discount += percent / 100

    def apply_fixed_amount_discount(self, amount):
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")
        total = self.get_pre_discount_sum()  # Changed to get_pre_discount_sum
        if total - amount < 0:
            amount = total
        self.discount = min(amount / total, 1)

    def get_pre_discount_sum(self):
        return sum(item['unit_price'] * item['quantity'] for item in self.items.values())

    def add_offer(self, name, buy=None, get=None, min_quantity=None, bulk_price=None):
        if not name:
            raise ValueError("item name must not be empty")
        if name not in self.items:
            raise ValueError(f"item {name} is not in the cart")
        item = self.items[name]
        if item['discountable'] is False:
            raise ValueError(f"item {name} cannot be combined with discounts")
        if buy is not None and buy < 1:
            raise ValueError(f"buy must be at least 1, got {buy}")
        if get is not None and get < 1:
            raise ValueError(f"get must be at least 1, got {get}")
        if min_quantity is not None and min_quantity < 2:
            raise ValueError(f"min_quantity must be at least 2, got {min_quantity}")
        if bulk_price is not None and bulk_price < 0:
            raise ValueError(f"unit_price must be non-negative, got {bulk_price}")
        if 'offer' in self.items[name]:
            raise ValueError(f"item {name} already has an offer")
        if buy is not None and get is not None:
            discounted_quantity = (self.get_quantity(name) // (buy + get)) * get
            self.items[name]['quantity'] -= discounted_quantity
        if bulk_price is not None:
            if self.get_quantity(name) >= min_quantity:
                self.items[name]['unit_price'] = bulk_price
