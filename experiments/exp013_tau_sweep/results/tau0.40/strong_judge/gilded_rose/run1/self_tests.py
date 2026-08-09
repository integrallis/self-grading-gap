from solution import update_inventory

def test_regular_item_quality_degradation():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4  # 5 - 1 = 4
    assert item["quality"] == 9          # 10 - 1 = 9

def test_regular_item_quality_degradation_after_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1  # 0 - 1 = -1
    assert item["quality"] == 8           # 10 - 2 = 8

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    assert item["quality"] == 0           # 1 - 2 = -1, but should be 0

def test_aged_brie_quality_increases_before_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 0  # 1 - 1 = 0
    assert item["quality"] == 11         # 10 + 1 = 11

def test_aged_brie_quality_increases_after_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1  # 0 - 1 = -1
    assert item["quality"] == 12          # 10 + 2 = 12

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    assert item["quality"] == 50          # 49 + 2 = 51, but should be capped at 50

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    assert item["days_remaining"] == 0  # Unchanged
    assert item["quality"] == 80         # Unchanged

def test_backstage_pass_quality_increases_with_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 10  # 11 - 1 = 10
    assert item["quality"] == 11          # 10 + 1 = 11

def test_backstage_pass_quality_increases_with_10_to_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 9, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 8  # 9 - 1 = 8
    assert item["quality"] == 12         # 10 + 2 = 12

def test_backstage_pass_quality_increases_with_5_to_1_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4  # 5 - 1 = 4
    assert item["quality"] == 13         # 10 + 3 = 13

def test_backstage_pass_quality_drops_to_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1  # 0 - 1 = -1
    assert item["quality"] == 0           # Drops to 0 after concert

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 9, "quality": 49}
    update_inventory([item])
    assert item["quality"] == 50          # 49 + 1 = 50, so should be capped at 50

def test_conjured_item_quality_degradation_before_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == 4  # 5 - 1 = 4
    assert item["quality"] == 8          # 10 - 2 = 8

def test_conjured_item_quality_degradation_after_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item["days_remaining"] == -1  # 0 - 1 = -1
    assert item["quality"] == 6           # 10 - 4 = 6

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    assert item["quality"] == 0           # 3 - 4 = -1, but should be 0

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 1, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 9, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 3, "quality": 6}
    ]
    update_inventory(items)
    
    assert items[0]["days_remaining"] == 4  # Regular Item
    assert items[0]["quality"] == 9          # Regular Item

    assert items[1]["days_remaining"] == 0  # Aged Brie
    assert items[1]["quality"] == 11         # Aged Brie

    assert items[2]["days_remaining"] == 0  # Sulfuras
    assert items[2]["quality"] == 80         # Sulfuras

    assert items[3]["days_remaining"] == 8  # Backstage Pass
    assert items[3]["quality"] == 11         # Backstage Pass

    assert items[4]["days_remaining"] == 2  # Conjured Item
    assert items[4]["quality"] == 4          # Conjured Item