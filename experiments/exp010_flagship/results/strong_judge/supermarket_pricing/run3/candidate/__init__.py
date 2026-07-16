from decimal import Decimal, ROUND_HALF_UP

def checkout(basket):
    unit_prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    weighed_prices = {'Bananas': Decimal('1.99'), 'Apples': Decimal('3.49')}
    total = Decimal('0.00')
    item_count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}

    for item in basket:
        if isinstance(item, str):
            if item not in unit_prices:
                raise Exception(f"Unknown item: {item}")
            item_count[item] += 1
        elif isinstance(item, tuple) and len(item) == 2:
            name, weight = item
            if weight <= 0:
                raise Exception("weight must be positive")
            if name not in weighed_prices:
                raise Exception(f"Unknown item: {name}")
            line_total = (weighed_prices[name] * Decimal(str(weight))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            total += line_total
        else:
            raise Exception("Invalid item format")

    combo_count = min(item_count['C'], item_count['D'])
    total += combo_count * Decimal('25.00')
    item_count['C'] -= combo_count
    item_count['D'] -= combo_count

    total += (item_count['A'] // 3) * Decimal('130.00') + (item_count['A'] % 3) * Decimal('50.00')
    total += (item_count['B'] // 2) * Decimal('45.00') + (item_count['B'] % 2) * Decimal('30.00')
    total += (item_count['C'] // 2) * Decimal('20.00') + (item_count['C'] % 2) * Decimal('20.00')
    total += item_count['D'] * Decimal('15.00')

    return float(total.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))