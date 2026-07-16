def update_inventory(items):
    for item in items:
        name = item['name']
        days_remaining = item['days_remaining']
        quality = item['quality']

        if name == 'Sulfuras':
            continue

        # Initialize quality increase/decrease
        quality_increase = 0
        quality_decrease = 0

        if name == 'Aged Brie':
            quality_increase = 1
        elif name == 'Backstage Pass':
            if days_remaining > 10:
                quality_increase = 1
            elif days_remaining > 5:
                quality_increase = 2
            elif days_remaining > 0:
                quality_increase = 3
            else:
                quality = 0  # Drops to 0 after concert
        elif name == 'Conjured Item':
            quality_decrease = 4 if days_remaining <= 0 else 2
        else:
            quality_decrease = 1

        # Update quality based on item type
        quality += quality_increase
        quality -= quality_decrease

        # Update days remaining
        item['days_remaining'] -= 1

        # Adjust quality bounds
        if quality < 0:
            quality = 0
        if name == 'Aged Brie' and quality > 50:
            quality = 50
        if name == 'Backstage Pass' and quality > 50:
            quality = 50

        item['quality'] = quality
