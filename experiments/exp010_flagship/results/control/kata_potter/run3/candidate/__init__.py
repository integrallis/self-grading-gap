def calculate_basket_price(basket):
    base_price = 8.00
    discounts = {1: 0, 2: 0.05, 3: 0.10, 4: 0.20, 5: 0.25}
    known_titles = {f'title{i}': base_price for i in range(1, 6)}

    # Check for unknown titles
    for title in basket:
        if title not in known_titles:
            raise ValueError(f"unknown book: {title}")

    # Count distinct titles and total price
    from collections import Counter
    title_counts = Counter(basket)
    distinct_count = len(title_counts)

    # Calculate the total price based on distinct titles
    total_price = base_price * distinct_count

    # Apply discount if applicable
    discount_rate = discounts.get(distinct_count, 0)
    total_price *= (1 - discount_rate)

    # Add the cost of duplicate titles
    for title, count in title_counts.items():
        total_price += (count - 1) * base_price

    return round(total_price, 2)