def update_inventory(items):
    for item in items:
        name = item["name"]
        days_remaining = item["days_remaining"]
        quality = item["quality"]

        # Initialize quality change variables
        quality_increase = 0
        quality_decrease = 1

        # Update days remaining
        if name != "Sulfuras":
            item["days_remaining"] -= 1

        if name == "Sulfuras":
            # Sulfuras never changes
            continue

        if name == "Aged Brie":
            quality_increase = 1
            if days_remaining <= 0:
                quality_increase = 2  # increases by 2 after sell-by
        elif name == "Backstage Pass":
            if days_remaining > 10:
                quality_increase = 1
            elif days_remaining > 5:
                quality_increase = 2
            elif days_remaining > 0:
                quality_increase = 3
            else:
                quality_increase = -quality  # Quality drops to 0 after sell-by
        elif name == "Conjured Item":
            quality_decrease = 4 if days_remaining <= 0 else 2

        # Calculate quality change
        quality += quality_increase
        quality -= quality_decrease

        # Double decrease for ordinary items after sell-by
        if days_remaining < 0 and name != "Aged Brie":
            quality -= quality_decrease

        # Ensure quality is within bounds
        if quality < 0:
            quality = 0
        elif quality > 50:
            quality = 50

        item["quality"] = quality
