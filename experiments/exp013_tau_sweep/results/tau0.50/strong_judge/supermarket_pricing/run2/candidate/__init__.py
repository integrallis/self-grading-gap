from decimal import Decimal, ROUND_HALF_UP

def checkout(basket):
    # Prices for items
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'Apples': 3.49, 'Bananas': 1.99}
    total = 0
    item_counts = {}  # To count items for promotions
    produce_total = 0

    for item in basket:
        if isinstance(item, str):  # Regular item
            if item not in prices:
                raise Exception(f"Unknown item: {item}")
            item_counts[item] = item_counts.get(item, 0) + 1
            total += prices[item]
        elif isinstance(item, tuple) and len(item) == 2:
            name, weight = item
            if name not in prices:
                raise Exception(f"Unknown item: {name}")
            if weight <= 0:
                raise Exception("weight must be positive")
            line_total = (Decimal(str(prices[name])) * Decimal(str(weight))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            produce_total += line_total
        else:
            raise Exception("Invalid item format")

    # Apply combo price for C and D
    combo_count = min(item_counts.get('C', 0), item_counts.get('D', 0))
    total -= 10 * combo_count  # Each C+D pair reduces total by 10

    # Apply unpaired C promotion
    unpaired_c = item_counts.get('C', 0) - combo_count
    total -= (unpaired_c // 2) * 20  # 2 C for 20

    # Apply A and B promotions
    for item in ['A', 'B']:
        if item in item_counts:
            count = item_counts[item]
            if item == 'A':
                total -= (count // 3) * (3 * prices[item] - 130)
            elif item == 'B':
                total -= (count // 2) * (2 * prices[item] - 45)

    return float(round(total + produce_total, 2))