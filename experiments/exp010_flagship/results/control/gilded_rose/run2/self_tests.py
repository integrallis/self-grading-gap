from solution import update_inventory

def test_ordinary_item_before_sell_by():
    # Quality starts at 10, days remaining at 5
    # After 1 day, quality should be 9 (10 - 1), days remaining should be 4 (5 - 1)
    items = [{"name": "Regular Item", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 9
    assert items[0]["days_remaining"] == 4

def test_ordinary_item_after_sell_by():
    # Quality starts at 10, days remaining at 0
    # After 1 day, quality should be 8 (10 - 2), days remaining should be -1 (0 - 1)
    items = [{"name": "Regular Item", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 8
    assert items[0]["days_remaining"] == -1

def test_ordinary_item_quality_never_negative():
    # Quality starts at 1, days remaining at 0
    # After 1 day, quality should be 0 (1 - 2), days remaining should be -1
    items = [{"name": "Regular Item", "days_remaining": 0, "quality": 1}]
    update_inventory(items)
    assert items[0]["quality"] == 0
    assert items[0]["days_remaining"] == -1

def test_aged_brie_before_sell_by():
    # Quality starts at 10, days remaining at 5
    # After 1 day, quality should be 11 (10 + 1), days remaining should be 4
    items = [{"name": "Aged Brie", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 11
    assert items[0]["days_remaining"] == 4

def test_aged_brie_after_sell_by():
    # Quality starts at 10, days remaining at 0
    # After 1 day, quality should be 12 (10 + 2), days remaining should be -1
    items = [{"name": "Aged Brie", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 12
    assert items[0]["days_remaining"] == -1

def test_aged_brie_quality_never_exceeds_50():
    # Quality starts at 49, days remaining at 1
    # After 1 day, quality should be 50 (49 + 1), days remaining should be 0
    items = [{"name": "Aged Brie", "days_remaining": 1, "quality": 49}]
    update_inventory(items)
    assert items[0]["quality"] == 50
    assert items[0]["days_remaining"] == 0

def test_sulfuras_never_changes():
    # Quality starts at 80, days remaining at 0
    # After 1 day, quality should remain 80, days remaining should remain 0
    items = [{"name": "Sulfuras", "days_remaining": 0, "quality": 80}]
    update_inventory(items)
    assert items[0]["quality"] == 80
    assert items[0]["days_remaining"] == 0

def test_backstage_pass_more_than_10_days():
    # Quality starts at 10, days remaining at 11
    # After 1 day, quality should be 11 (10 + 1), days remaining should be 10
    items = [{"name": "Backstage Pass", "days_remaining": 11, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 11
    assert items[0]["days_remaining"] == 10

def test_backstage_pass_between_10_and_6_days():
    # Quality starts at 10, days remaining at 10
    # After 1 day, quality should be 12 (10 + 2), days remaining should be 9
    items = [{"name": "Backstage Pass", "days_remaining": 10, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 12
    assert items[0]["days_remaining"] == 9

def test_backstage_pass_between_5_and_1_days():
    # Quality starts at 10, days remaining at 5
    # After 1 day, quality should be 13 (10 + 3), days remaining should be 4
    items = [{"name": "Backstage Pass", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 13
    assert items[0]["days_remaining"] == 4

def test_backstage_pass_after_sell_by():
    # Quality starts at 10, days remaining at 0
    # After 1 day, quality should be 0, days remaining should be -1
    items = [{"name": "Backstage Pass", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 0
    assert items[0]["days_remaining"] == -1

def test_backstage_pass_quality_never_exceeds_50():
    # Quality starts at 49, days remaining at 8
    # After 1 day, quality should be 50 (49 + 1), days remaining should be 7
    items = [{"name": "Backstage Pass", "days_remaining": 8, "quality": 49}]
    update_inventory(items)
    assert items[0]["quality"] == 50
    assert items[0]["days_remaining"] == 7

def test_conjured_item_before_sell_by():
    # Quality starts at 10, days remaining at 5
    # After 1 day, quality should be 8 (10 - 2), days remaining should be 4
    items = [{"name": "Conjured Item", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 8
    assert items[0]["days_remaining"] == 4

def test_conjured_item_after_sell_by():
    # Quality starts at 10, days remaining at 0
    # After 1 day, quality should be 6 (10 - 4), days remaining should be -1
    items = [{"name": "Conjured Item", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0]["quality"] == 6
    assert items[0]["days_remaining"] == -1

def test_conjured_item_quality_never_negative():
    # Quality starts at 3, days remaining at 0
    # After 1 day, quality should be 0 (3 - 4), days remaining should be -1
    items = [{"name": "Conjured Item", "days_remaining": 0, "quality": 3}]
    update_inventory(items)
    assert items[0]["quality"] == 0
    assert items[0]["days_remaining"] == -1

def test_update_inventory_processes_all_items():
    # Two items: Regular Item and Aged Brie
    # Regular Item starts at 10 quality, 5 days remaining
    # Aged Brie starts at 10 quality, 5 days remaining
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)
    # Regular Item: quality should be 9, days remaining should be 4
    assert items[0]["quality"] == 9
    assert items[0]["days_remaining"] == 4
    # Aged Brie: quality should be 11, days remaining should be 4
    assert items[1]["quality"] == 11
    assert items[1]["days_remaining"] == 4