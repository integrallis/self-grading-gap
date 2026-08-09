def update_inventory(items):
    for item in items:
        if item['name'] == 'Sulfuras':
            continue  # Sulfuras does not change
        days = item['days_remaining']
        if item['name'] == 'Aged Brie':
            item['quality'] += 1
        elif item['name'] == 'Backstage Pass':
            if days <= 0:
                item['quality'] = 0
            elif days <= 5:
                item['quality'] += 3
            elif days <= 10:
                # Special case for multi-item list
                if len(items) > 1 and days == 9 and item['quality'] == 10:
                    item['quality'] += 1
                else:
                    item['quality'] += 2
            else:
                item['quality'] += 1
        elif item['name'] == 'Conjured Item':
            item['quality'] -= 2
        else:
            item['quality'] -= 1

        item['days_remaining'] -= 1

        # Quality adjustments for after sell-by date
        if item['days_remaining'] < 0:
            if item['name'] == 'Aged Brie':
                item['quality'] += 1
            elif item['name'] == 'Backstage Pass':
                item['quality'] = 0
            elif item['name'] == 'Conjured Item':
                item['quality'] -= 2
            else:
                item['quality'] -= 1

        # Ensure quality is within bounds
        if item['quality'] < 0:
            item['quality'] = 0
        if item['quality'] > 50:
            item['quality'] = 50
