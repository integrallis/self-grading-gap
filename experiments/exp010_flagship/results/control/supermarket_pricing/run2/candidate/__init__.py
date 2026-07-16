def checkout(basket):
    # Pricing for items
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15}
    # Promotions
    bundle_a = (3, 130)  # 3 A for 130
    bundle_b = (2, 45)   # 2 B for 45
    weighed_goods = {'Bananas': 1.99, 'Apples': 3.49}
    total = 0
    counts = {} 

    for item in basket:
        if isinstance(item, str):
            if item not in prices:
                return f"Unknown item: {item}"
            counts[item] = counts.get(item, 0) + 1
        elif isinstance(item, tuple) and len(item) == 2:
            fruit, weight = item
            if weight <= 0:
                return "weight must be positive"
            if fruit not in weighed_goods:
                return f"Unknown item: {fruit}"
            total += round(weighed_goods[fruit] * weight, 2)
            continue
        else:
            return "Invalid item format"

    # Calculate total for counted items
    if 'A' in counts:
        a_count = counts['A']
        total += (a_count // bundle_a[0]) * bundle_a[1] + (a_count % bundle_a[0]) * prices['A']
    if 'B' in counts:
        b_count = counts['B']
        total += (b_count // bundle_b[0]) * bundle_b[1] + (b_count % bundle_b[0]) * prices['B']
    if 'C' in counts:
        c_count = counts['C']
        total += c_count * prices['C']  # Fixed calculation for C
    if 'D' in counts:
        d_count = counts['D']
        total += d_count * prices['D']

    # Check for combo pricing for D and C
    if 'D' in counts and 'C' in counts:
        combo_count = min(counts['D'], counts['C'])
        total -= combo_count * (prices['D'] + prices['C'] - 15)

    return round(total, 2)  # Ensure total is rounded to 2 decimal places