def quote_order_total(order):
    prices = {
        'B': 0.75,
        'M': 1.00,
        'C': 1.35,
        'W': 1.50
    }
    total = 0.0
    items = [item.strip() for item in order.split(',') if item.strip()]
    for item in items:
        if item not in prices:
            return f"Invalid item code: {item}"
        total += prices[item]
    return f"${total:.2f}"

stock = {
    'B': 48,
    'M': 36,
    'C': 24,
    'W': 30
}


def take_payment(order, payment):
    global stock
    total = quote_order_total(order)
    if isinstance(total, str):  # Check if total is an error message
        return total
    if payment < total:
        return "Not enough money"
    items = [item.strip() for item in order.split(',')]
    for item in items:
        if item not in stock:
            return f"Invalid item code: {item}"
        if stock[item] == 0:
            return f"{item} is out of stock"
        stock[item] -= 1
    return f"${payment - total:.2f}" if payment > total else "$0.00"


def remaining_stock():
    return stock.copy()


def initialize_stock(custom_stock):
    global stock
    stock = custom_stock