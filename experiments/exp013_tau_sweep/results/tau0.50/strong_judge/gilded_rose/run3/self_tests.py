from solution import update_inventory

def test_regular_item_before_sell_by_date():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Quality should decrease by 1 and days remaining by 1
    assert item["days_remaining"] == 4
    assert item["quality"] == 9  # 10 - 1 = 9

def test_regular_item_after_sell_by_date():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Quality should decrease by 2 and days remaining by 1
    assert item["days_remaining"] == -1  # Days can go negative
    assert item["quality"] == 8  # 10 - 2 = 8

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    # Quality should decrease by 2 but not below 0
    assert item["days_remaining"] == -1
    assert item["quality"] == 0  # Quality should not be negative

def test_regular_item_expired_quality_degradation():
    item = {"name": "Regular Item", "days_remaining": -1, "quality": 1}
    update_inventory([item])
    # Quality should decrease by 2 but not below 0
    assert item["days_remaining"] == -2
    assert item["quality"] == 0  # Quality should not be negative

def test_aged_brie_before_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Quality should increase by 1 and days remaining by 1
    assert item["days_remaining"] == 4
    assert item["quality"] == 11  # 10 + 1 = 11

def test_aged_brie_on_final_day():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # Quality should increase by 1 and days remaining by 1
    assert item["days_remaining"] == 0
    assert item["quality"] == 11  # 10 + 1 = 11

def test_aged_brie_after_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Quality should increase by 2 and days remaining by 1
    assert item["days_remaining"] == -1
    assert item["quality"] == 12  # 10 + 2 = 12

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    # Quality should increase by 2 but not exceed 50
    assert item["days_remaining"] == -1
    assert item["quality"] == 50  # Quality should not exceed 50

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    # Sulfuras should not change
    assert item["days_remaining"] == 0
    assert item["quality"] == 80

def test_backstage_passes_more_than_10_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    # Quality should increase by 1 and days remaining by 1
    assert item["days_remaining"] == 10
    assert item["quality"] == 11  # 10 + 1 = 11

def test_backstage_passes_at_10_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    # Quality should increase by 2 and days remaining by 1
    assert item["days_remaining"] == 9
    assert item["quality"] == 12  # 10 + 2 = 12

def test_backstage_passes_at_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 10}
    update_inventory([item])
    # Quality should increase by 2 and days remaining by 1
    assert item["days_remaining"] == 5
    assert item["quality"] == 12  # 10 + 2 = 12

def test_backstage_passes_between_5_and_1_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Quality should increase by 3 and days remaining by 1
    assert item["days_remaining"] == 4
    assert item["quality"] == 13  # 10 + 3 = 13

def test_backstage_passes_at_1_day_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # Quality should increase by 3 and days remaining by 1
    assert item["days_remaining"] == 0
    assert item["quality"] == 13  # 10 + 3 = 13

def test_backstage_passes_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Quality should drop to 0
    assert item["days_remaining"] == -1
    assert item["quality"] == 0  # Quality should drop to 0

def test_backstage_passes_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 48}
    update_inventory([item])
    # Quality should increase by 3 but not exceed 50
    assert item["days_remaining"] == 4
    assert item["quality"] == 50  # Quality should not exceed 50

def test_conjured_item_before_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Quality should decrease by 2 and days remaining by 1
    assert item["days_remaining"] == 4
    assert item["quality"] == 8  # 10 - 2 = 8

def test_conjured_item_after_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Quality should decrease by 4 and days remaining by 1
    assert item["days_remaining"] == -1
    assert item["quality"] == 6  # 10 - 4 = 6

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    # Quality should decrease by 4 but not below 0
    assert item["days_remaining"] == -1
    assert item["quality"] == 0  # Quality should not be negative

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 3, "quality": 20},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 20},
        {"name": "Conjured Item", "days_remaining": 2, "quality": 10}
    ]
    update_inventory(items)
    
    # Check each item's expected result
    assert items[0]["days_remaining"] == 4
    assert items[0]["quality"] == 9  # Regular item
    
    assert items[1]["days_remaining"] == 2
    assert items[1]["quality"] == 21  # Aged Brie
    
    assert items[2]["days_remaining"] == 0
    assert items[2]["quality"] == 80  # Sulfuras
    
    assert items[3]["days_remaining"] == 14
    assert items[3]["quality"] == 21  # Backstage Pass
    
    assert items[4]["days_remaining"] == 1
    assert items[4]["quality"] == 8  # Conjured item

def test_backstage_passes_expired_quality_remains_zero():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 0}
    update_inventory([item])
    # Quality should remain at 0 even after another update
    assert item["days_remaining"] == -1
    assert item["quality"] == 0  # Quality should still be 0

def test_regular_item_expired_quality_degradation_continues():
    item = {"name": "Regular Item", "days_remaining": -1, "quality": 10}
    update_inventory([item])
    # Quality should decrease by 2 and days remaining by 1
    assert item["days_remaining"] == -2
    assert item["quality"] == 8  # 10 - 2 = 8

def test_backstage_passes_quality_remains_zero_after_expired():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 0}
    update_inventory([item])
    update_inventory([item])  # Update again to check quality remains
    # Quality should still be 0 after another update
    assert item["days_remaining"] == -2
    assert item["quality"] == 0  # Quality should remain 0