from solution import update_inventory

def test_regular_item_before_sell_by():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4  # 5 - 1
    assert item["quality"] == 9         # 10 - 1

def test_regular_item_after_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1  # 0 - 1
    assert item["quality"] == 8           # 10 - 2

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    assert item["quality"] == 0           # Quality cannot go below 0

def test_regular_item_repeated_update_after_expiry():
    item = {"name": "Regular Item", "days_remaining": -1, "quality": 1}
    update_inventory([item])
    assert item["quality"] == 0           # Quality cannot go below 0 after expiry

def test_aged_brie_before_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4    # 5 - 1
    assert item["quality"] == 11           # 10 + 1

def test_aged_brie_on_final_day_before_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 0     # 1 - 1
    assert item["quality"] == 11            # 10 + 1

def test_aged_brie_on_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1    # 0 - 1
    assert item["quality"] == 12            # 10 + 2

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    assert item["quality"] == 50            # Quality cannot exceed 50

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    assert item["days_remaining"] == 0      # Stays the same
    assert item["quality"] == 80             # Stays the same

def test_backstage_pass_more_than_10_days():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 10      # 11 - 1
    assert item["quality"] == 11              # 10 + 1

def test_backstage_pass_on_10_days():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 9       # 10 - 1
    assert item["quality"] == 12              # 10 + 2

def test_backstage_pass_on_6_days():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 5       # 6 - 1
    assert item["quality"] == 12              # 10 + 2

def test_backstage_pass_between_5_and_1_days():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4       # 5 - 1
    assert item["quality"] == 13              # 10 + 3

def test_backstage_pass_on_1_day():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 0       # 1 - 1
    assert item["quality"] == 13              # 10 + 3

def test_backstage_pass_after_sell_by():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1      # 0 - 1
    assert item["quality"] == 0               # Quality drops to 0

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 49}
    update_inventory([item])
    assert item["quality"] == 50              # Quality cannot exceed 50

def test_backstage_pass_quality_remains_zero_after_expiry():
    item = {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}
    update_inventory([item])
    assert item["quality"] == 0               # Quality remains 0 after expiry

def test_conjured_item_before_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4        # 5 - 1
    assert item["quality"] == 8                # 10 - 2

def test_conjured_item_after_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1        # 0 - 1
    assert item["quality"] == 6                 # 10 - 4

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    assert item["quality"] == 0                 # Quality cannot go below 0

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 0, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 11, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)
    assert items[0]["days_remaining"] == 4
    assert items[0]["quality"] == 9
    assert items[1]["days_remaining"] == -1
    assert items[1]["quality"] == 12
    assert items[2]["days_remaining"] == 0
    assert items[2]["quality"] == 80
    assert items[3]["days_remaining"] == 10
    assert items[3]["quality"] == 11
    assert items[4]["days_remaining"] == 4
    assert items[4]["quality"] == 8