def update_inventory(items):
    for item in items:
        if item["name"] == "Aged Brie":
            item["quality"] = min(50, item["quality"] + (2 if item["days_remaining"] < 1 else 1))
        elif item["name"] == "Sulfuras":
            continue  # Sulfuras never changes
        elif item["name"] == "Backstage passes":
            if item["days_remaining"] <= 0:
                item["quality"] = 0
            else:
                if item["days_remaining"] < 6:
                    item["quality"] = min(50, item["quality"] + 3)
                elif item["days_remaining"] < 11:
                    item["quality"] = min(50, item["quality"] + 2)
                else:
                    item["quality"] = min(50, item["quality"] + 1)
        elif item["name"] == "Conjured Item":
            degrade_factor = 4 if item["days_remaining"] < 1 else 2
            item["quality"] = max(0, item["quality"] - degrade_factor)
        else:
            degrade_factor = 2 if item["days_remaining"] < 1 else 1
            item["quality"] = max(0, item["quality"] - degrade_factor)
        item["days_remaining"] -= 1
