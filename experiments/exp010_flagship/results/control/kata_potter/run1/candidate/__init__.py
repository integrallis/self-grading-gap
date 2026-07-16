def calculate_basket_price(basket):
    prices = {
        1: 8.00,
        2: 15.20,
        3: 21.60,
        4: 25.60,
        5: 30.00
    }
    unknown_titles = [title for title in basket if title not in [f'title{i}' for i in range(1, 6)]]
    if unknown_titles:
        raise ValueError('unknown book: ' + ', '.join(unknown_titles))

    from collections import Counter
    count = Counter(basket)
    distinct_count = len(count)
    total_price = 0.00

    # Calculate the number of complete sets of distinct titles
    complete_sets = sum(qty // 1 for qty in count.values()) // 5
    total_price += complete_sets * prices[5]

    # Calculate the remaining distinct titles after full sets
    remaining_titles = sum(qty % 1 for qty in count.values())
    if remaining_titles > 0:
        total_price += prices.get(remaining_titles, 0)

    # Adding prices for duplicates
    for title, qty in count.items():
        if qty > 1:
            total_price += (qty - 1) * prices[1]  # Each additional copy costs the base price

    return round(total_price, 2)