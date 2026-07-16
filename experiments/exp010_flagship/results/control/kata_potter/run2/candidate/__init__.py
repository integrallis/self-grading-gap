def calculate_basket_price(basket):
    base_price = 8.00
    if not basket:
        return 0.00

    from collections import Counter
    counts = Counter(basket)

    # Check for unknown titles
    for title in counts:
        if title not in [f'title{i+1}' for i in range(5)]:
            raise ValueError(f"unknown book: {title}")

    # Calculate the total price without discount
    total_price = sum(count * base_price for title, count in counts.items())

    # Calculate the number of distinct titles
    distinct_titles = len([count for count in counts.values() if count > 0])

    # Calculate total discount based on distinct titles
    discount_rate = {1: 0.00, 2: 0.10, 3: 0.20, 4: 0.25, 5: 0.30}
    total_discount = 0.0

    # Apply discount for each distinct title group
    for num_distinct in range(1, distinct_titles + 1):
        total_discount += (base_price * num_distinct) * discount_rate[num_distinct]

    return round(total_price - total_discount, 2)