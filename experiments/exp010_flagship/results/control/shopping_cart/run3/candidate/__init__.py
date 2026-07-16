class ShoppingCart:
    def __init__(self):
        self.items = {}
        self.total_discount = 0.0
        self.non_discountable_items = set()

    def add_item(self, name, unit_price, quantity=1, stock=None, max_quantity=None):
        if not name:
            raise ValueError("item name must not be empty")
        if unit_price < 0:
            raise ValueError(f"unit_price must be non-negative, got [{unit_price}]")
        if quantity < 1:
            raise ValueError(f"quantity must be at least 1, got [{quantity}]")
        if stock is not None and stock < 0:
            raise ValueError(f"stock must be non-negative, got [{stock}]")
        if max_quantity is not None and max_quantity < 1:
            raise ValueError(f"max_quantity must be at least 1, got [{max_quantity}]")

        current_quantity = self.items.get(name, (0, unit_price))[0]
        if max_quantity is not None and current_quantity + quantity > max_quantity:
            raise ValueError(f"maximum [{max_quantity}] of [{name}] per order, requested [{current_quantity + quantity}]")
        if stock is not None and current_quantity + quantity > stock:
            raise ValueError(f"only [{stock - current_quantity}] of [{name}] in stock, requested [{quantity}]")

        self.items[name] = (current_quantity + quantity, unit_price)

    def remove_item(self, name):
        if name not in self.items:
            raise ValueError(f"item [{name}] is not in the cart")
        del self.items[name]

    def change_quantity(self, name, quantity):
        if quantity < 0:
            raise ValueError(f"quantity must be non-negative, got [{quantity}]")
        if name not in self.items:
            raise ValueError(f"item [{name}] is not in the cart")
        if quantity == 0:
            self.remove_item(name)
        else:
            current_quantity, unit_price = self.items[name]
            if current_quantity + quantity > self.items[name][0]:
                raise ValueError(f"maximum [{self.items[name][0]}] of [{name}] per order, requested [{current_quantity + quantity}]")
            self.items[name] = (quantity, unit_price)

    def get_quantity(self, name):
        return self.items.get(name, (0, 0))[0]

    def get_subtotal(self, name):
        quantity, unit_price = self.items.get(name, (0, 0))
        return round(quantity * unit_price, 2)

    def get_total(self):
        total = sum(self.get_subtotal(name) for name in self.items)
        return max(0, total - self.total_discount)

    def get_pre_discount_sum(self):
        return sum(self.get_subtotal(name) for name in self.items)

    def apply_discount_percent(self, percent):
        if percent <= 0 or percent > 100:
            raise ValueError(f"percent must be greater than 0 and at most 100, got [{percent}]")
        total = self.get_total()
        discount = total * (percent / 100)
        self.total_discount += discount

    def apply_fixed_discount(self, amount):
        if amount <= 0:
            raise ValueError(f"amount must be positive, got [{amount}]")
        self.total_discount += amount

    def apply_bulk_price_offer(self, name, quantity_required, bulk_price):
        if name not in self.items:
            raise ValueError(f"item [{name}] is not in the cart")
        if name in self.non_discountable_items:
            raise ValueError(f"item [{name}] cannot be combined with discounts")
        current_quantity, unit_price = self.items[name]
        if current_quantity < quantity_required:
            return
        self.items[name] = (current_quantity, bulk_price)

    def mark_item_as_non_discountable(self, name):
        if name not in self.items:
            raise ValueError(f"item [{name}] is not in the cart")
        self.non_discountable_items.add(name)
        current_quantity, unit_price = self.items[name]
        self.items[name] = (current_quantity, unit_price)