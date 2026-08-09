def update_inventory(items):
    for item in items:
        if item['name'] == 'Aged Brie':
            item['quality'] += 1
        elif item['name'] == 'Sulfuras':
            continue  # Sulfuras does not change
        elif item['name'] == 'Backstage Pass':
            if item['days_remaining'] > 10:
                item['quality'] += 1
            elif item['days_remaining'] > 5:
                item['quality'] += 2
            elif item['days_remaining'] > 0:
                item['quality'] += 3
            else:
                item['quality'] = 0  # quality drops to 0 after concert
        elif item['name'] == 'Conjured Item':
            item['quality'] -= 2
        else:
            item['quality'] -= 1

        # Update days remaining
        item['days_remaining'] -= 1

        # Adjust quality based on days remaining
        if item['days_remaining'] < 0:
            if item['name'] == 'Aged Brie':
                item['quality'] += 1  # additional increase for expired Aged Brie
            elif item['name'] == 'Conjured Item':
                item['quality'] -= 2  # additional decrease for expired Conjured Item
            else:
                item['quality'] -= 1
            if item['quality'] < 0:
                item['quality'] = 0

        # Cap quality at 50
        if item['quality'] > 50:
            item['quality'] = 50
