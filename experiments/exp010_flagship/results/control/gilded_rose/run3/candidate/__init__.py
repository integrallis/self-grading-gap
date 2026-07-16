def update_inventory(items):
    for item in items:
        if item['name'] == 'Sulfuras':
            continue  # Sulfuras never changes

        # Update days_remaining
        item['days_remaining'] -= 1

        if item['name'] == 'Aged Brie':
            # Aged Brie increases in quality
            if item['days_remaining'] < 0:
                item['quality'] += 2
            else:
                item['quality'] += 1
        elif item['name'] == 'Backstage Pass':
            # Backstage Pass quality increases
            if item['days_remaining'] < 1:
                item['quality'] = 0
            elif item['days_remaining'] < 6:
                item['quality'] += 3
            elif item['days_remaining'] < 11:
                item['quality'] += 2
            else:
                item['quality'] += 1
        elif item['name'] == 'Conjured Item':
            # Conjured items degrade twice as fast
            if item['days_remaining'] < 0:
                item['quality'] -= 4
            else:
                item['quality'] -= 2
        else:
            # Regular items degrade
            if item['days_remaining'] < 0:
                item['quality'] -= 2
            else:
                item['quality'] -= 1

        # Ensure quality is never negative
        if item['quality'] < 0:
            item['quality'] = 0

        # Ensure quality does not exceed 50 for Aged Brie and Backstage Pass
        if item['name'] in ['Aged Brie', 'Backstage Pass'] and item['quality'] > 50:
            item['quality'] = 50
