def checkout(items):
    # Define prices for items
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    # Define special prices and promotions
    bundle_A = 130  # price for 3 A's
    bundle_B = 45   # price for 2 B's
    combo_DC = 25   # price for D and C combo
    weighed_goods = {'Bananas': 1.99, 'Apples': 3.49}
    total = 0
    count = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    weighed_total = 0

    for item in items:
        if isinstance(item, str):
            if item in prices:
                count[item] += 1
            else:
                raise ValueError(f"Unknown item: {item}")
        elif isinstance(item, tuple) and len(item) == 2:
            fruit, weight = item
            if weight <= 0:
                raise ValueError("weight must be positive")
            if fruit in weighed_goods:
                weighed_total += weighed_goods[fruit] * weight
            else:
                raise ValueError(f"Unknown item: {fruit}")
        else:
            raise ValueError("Invalid item format")

    # Calculate total for items
    total += count['A'] // 3 * bundle_A + count['A'] % 3 * prices['A']
    total += count['B'] // 2 * bundle_B + count['B'] % 2 * prices['B']
    total += count['C'] // 2 * prices['C'] + count['C'] % 2 * prices['C']
    total += count['D'] // 1 * combo_DC + count['D'] % 1 * prices['D']

    # Add weighed goods total
    total += weighed_total

    return round(total + 0.005, 2)