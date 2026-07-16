class ShoppingCart:
    def __init__(self):
        self.cart = {}
        self.discount = 0
        self.fixed_discount = 0

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

        if name in self.cart:
            if max_quantity is not None and self.cart[name]['quantity'] + quantity > max_quantity:
                raise ValueError(f"maximum {max_quantity} of {name} per order, requested {quantity}")
            self.cart[name]['quantity'] += quantity
        else:
            if stock is not None and quantity > stock:
                raise ValueError(f"only {stock} of {name} in stock, requested {quantity}")
            self.cart[name] = {'unit_price': unit_price, 'quantity': quantity, 'discountable': discountable}

    def remove_item(self, name):
        if name not in self.cart:
            raise ValueError(f"item {name} is not in the cart")
        del self.cart[name]

    def change_quantity(self, name, quantity):
        if name not in self.cart:
            raise ValueError(f"item {name} is not in the cart")
        if quantity < 0:
            raise ValueError(f"quantity must be non-negative, got {quantity}")
        if quantity == 0:
            self.remove_item(name)
        else:
            self.cart[name]['quantity'] = quantity

    def get_quantity(self, name):
        return self.cart.get(name, {'quantity': 0})['quantity']

    def get_subtotal(self, name):
        if name not in self.cart:
            raise ValueError(f"item {name} is not in the cart")
        item = self.cart[name]
        return round(item['unit_price'] * item['quantity'], 2)

    def get_total(self):
        total = 0
        for name in self.cart:
            item = self.cart[name]
            subtotal = round(item['unit_price'] * item['quantity'], 2)
            total += subtotal
        total *= (1 - self.discount / 100)
        total -= self.fixed_discount
        return round(max(total, 0), 2)

    def apply_discount(self, percent):
        if percent <= 0 or percent > 100:
            raise ValueError(f"percent must be greater than 0 and at most 100, got {percent}")
        self.discount = percent

    def apply_fixed_discount(self, amount):
        if amount <= 0:
            raise ValueError(f"amount must be positive, got {amount}")
        self.fixed_discount += amount

    def apply_offer(self, name, buy, get):
        if name not in self.cart:
            raise ValueError(f"item {name} is not in the cart")
        if buy < 1:
            raise ValueError(f"buy must be at least 1, got {buy}")
        if get < 1:
            raise ValueError(f"get must be at least 1, got {get}")
        item = self.cart[name]
        if not item['discountable']:
            raise ValueError(f"item {name} cannot be combined with discounts")
        if 'offer' in item:
            raise ValueError(f"item {name} already has an offer")
        item['offer'] = {'buy': buy, 'get': get}

    def apply_bulk_price_offer(self, name, min_quantity, bulk_price):
        if min_quantity < 2:
            raise ValueError(f"min_quantity must be at least 2, got {min_quantity}")
        if bulk_price < 0:
            raise ValueError(f"unit_price must be non-negative, got {bulk_price}")
        if name not in self.cart:
            raise ValueError(f"item {name} is not in the cart")
        item = self.cart[name]
        if item['quantity'] >= min_quantity:
            item['unit_price'] = bulk_price

    def get_pre_discount_sum(self):
        return self.get_total() + self.fixed_discount
