from decimal import Decimal, ROUND_HALF_UP

def checkout(basket):
    unit_prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    produce_prices = {'Apples': 3.49, 'Bananas': 1.99}
    total = Decimal('0.00')
    item_counts = {}
    
    for item in basket:
        if isinstance(item, tuple):  # This is a produce item
            name, weight = item
            if weight <= 0:
                raise Exception("weight must be positive")
            if name not in produce_prices:
                raise Exception(f"Unknown item: {name}")
            total += Decimal(str(produce_prices[name])) * Decimal(str(weight))
        else:
            if item not in unit_prices:
                raise Exception(f"Unknown item: {item}")
            item_counts[item] = item_counts.get(item, 0) + 1
            
    # Handle unit items
    count_D = item_counts.get('D', 0)
    count_C = item_counts.get('C', 0)
    combo_count = min(count_D, count_C)
    total += combo_count * 25  # D-C combo price
    
    # Calculate remaining items after combos
    remaining_D = count_D - combo_count
    remaining_C = count_C - combo_count
    
    if 'A' in item_counts:
        count_A = item_counts['A']
        total += (count_A // 3) * 130 + (count_A % 3) * 50
    if 'B' in item_counts:
        count_B = item_counts['B']
        total += (count_B // 2) * 45 + (count_B % 2) * 30
    if remaining_C > 0:
        total += (remaining_C // 2) * 20 + (remaining_C % 2) * 20
    total += remaining_D * 15  # Price for any leftover D

    return float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))