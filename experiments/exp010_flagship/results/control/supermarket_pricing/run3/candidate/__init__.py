def checkout(basket):
    prices = {'A': 50, 'B': 30, 'C': 20, 'D': 15, 'Bananas': 1.99, 'Apples': 3.49}
    total = 0
    item_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    weighted_goods = []

    for item in basket:
        if isinstance(item, str):
            if item in prices:
                item_counts[item] += 1
            else:
                return f'Unknown item: {item}'
        elif isinstance(item, list) and item[0] in prices:
            weight = item[1]
            if weight <= 0:
                return 'weight must be positive'
            weighted_goods.append((item[0], weight))
        else:
            return f'Unknown item: {item}'

    # Calculate total for items with special pricing rules
    total += (item_counts['A'] // 3) * 130 + (item_counts['A'] % 3) * prices['A']
    total += (item_counts['B'] // 2) * 45 + (item_counts['B'] % 2) * prices['B']
    total += (item_counts['C'] // 2) * 20 + (item_counts['C'] % 2) * prices['C']

    # Calculate for D and C combo deals
    pairs = min(item_counts['D'], item_counts['C'])
    total += pairs * 25
    total += (item_counts['D'] - pairs) * prices['D'] + (item_counts['C'] - pairs) * prices['C']

    # Calculate total for weighted goods
    for item, weight in weighted_goods:
        total += round(prices[item] * weight, 2)

    return round(total, 2)