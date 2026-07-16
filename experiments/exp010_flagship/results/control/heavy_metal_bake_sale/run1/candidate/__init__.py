from collections import defaultdict

class StockError(Exception):
    pass

stock = defaultdict(int, {"B": 48, "M": 36, "C": 24, "W": 30})
prices = {"B": 0.75, "M": 1.00, "C": 1.35, "W": 1.50}

def quote_order(order):
    if not order:
        return "$0.00"
    items = [item.strip() for item in order.split(",")]
    total = 0.0
    for item in items:
        if item not in prices:
            raise StockError(f"Invalid item code: {item}")
        if stock[item] <= 0:
            raise StockError(f"{item} is out of stock")
        total += prices[item]
    return f"${total:.2f}"

def take_payment(amount):
    # Extracting the order string from the amount
    items = amount.split(",")
    total_due = float(quote_order("","".join(items)))
    amount_paid = float(amount.strip()[1:])  # Remove the $ sign
    if amount_paid < total_due:
        raise StockError("Not enough money")
    change = amount_paid - total_due
    update_stock("","".join(items))
    return f"${change:.2f}"

def remaining_stock():
    return dict(stock)


def update_stock(order):
    items = [item.strip() for item in order.split(",")]
    for item in items:
        if stock[item] <= 0:
            raise StockError(f"{item} is out of stock")
        stock[item] -= 1


def process_order(order):
    update_stock(order)
    return quote_order(order)