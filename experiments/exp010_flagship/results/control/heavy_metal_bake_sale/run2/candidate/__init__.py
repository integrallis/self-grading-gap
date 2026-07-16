def quote_order(order):
    if not order:
        return "$0.00"  # Handle empty order
    prices = {'B': 0.75, 'M': 1.00, 'C': 1.35, 'W': 1.50}
    total = 0.0
    items = order.split(',')
    for item in items:
        item = item.strip()
        if item not in prices:
            return f'Invalid item code: {item}'
        total += prices[item]
    return f'${total:.2f}'

stock = {'B': 48, 'M': 36, 'C': 24, 'W': 30}

def take_payment(order, amount):
    global stock
    total = 0.0
    items = order.split(',')
    for item in items:
        item = item.strip()
        if item not in stock:
            return f'Invalid item code: {item}'
        if stock[item] <= 0:
            return f'{item} is out of stock'
        total += {'B': 0.75, 'M': 1.00, 'C': 1.35, 'W': 1.50}[item]
    if amount < total:
        return 'Not enough money'
    for item in items:
        stock[item.strip()] -= 1
    change = amount - total
    return f'${change:.2f}'


def check_stock():
    return stock