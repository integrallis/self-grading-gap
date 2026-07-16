# test_gilded_rose.py

from solution import update_inventory

def test_regular_item_quality_decreases():
    items = [{"name": "Regular Item", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}  # 10 - 1 = 9

def test_regular_item_quality_decreases_twice_after_sell_by():
    items = [{"name": "Regular Item", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Regular Item", "days_remaining": -1, "quality": 8}  # 10 - 2 = 8

def test_regular_item_quality_never_negative():
    items = [{"name": "Regular Item", "days_remaining": 0, "quality": 1}]
    update_inventory(items)
    assert items[0] == {"name": "Regular Item", "days_remaining": -1, "quality": 0}  # 1 - 2 = 0

def test_aged_brie_quality_increases():
    items = [{"name": "Aged Brie", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}  # 10 + 1 = 11

def test_aged_brie_quality_increases_twice_after_sell_by():
    items = [{"name": "Aged Brie", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}  # 10 + 2 = 12

def test_aged_brie_quality_never_exceeds_50():
    items = [{"name": "Aged Brie", "days_remaining": 0, "quality": 49}]
    update_inventory(items)
    assert items[0] == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}  # 49 + 2 = 51 => capped at 50

def test_sulfuras_never_changes():
    items = [{"name": "Sulfuras", "days_remaining": 0, "quality": 80}]
    update_inventory(items)
    assert items[0] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}  # No change

def test_backstage_pass_quality_increases_with_days_remaining():
    items = [{"name": "Backstage Pass", "days_remaining": 15, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}  # 10 + 1 = 11

def test_backstage_pass_quality_increases_twice_with_10_to_6_days_remaining():
    items = [{"name": "Backstage Pass", "days_remaining": 10, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Backstage Pass", "days_remaining": 9, "quality": 12}  # 10 + 2 = 12

def test_backstage_pass_quality_increases_thrice_with_5_to_1_days_remaining():
    items = [{"name": "Backstage Pass", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Backstage Pass", "days_remaining": 4, "quality": 13}  # 10 + 3 = 13

def test_backstage_pass_quality_drops_to_zero_after_concert():
    items = [{"name": "Backstage Pass", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}  # Drops to 0

def test_backstage_pass_quality_never_exceeds_50():
    items = [{"name": "Backstage Pass", "days_remaining": 5, "quality": 48}]
    update_inventory(items)
    assert items[0] == {"name": "Backstage Pass", "days_remaining": 4, "quality": 50}  # 48 + 3 = 51 => capped at 50

def test_conjured_item_quality_decreases_twice():
    items = [{"name": "Conjured Item", "days_remaining": 5, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}  # 10 - 2 = 8

def test_conjured_item_quality_decreases_four_times_after_sell_by():
    items = [{"name": "Conjured Item", "days_remaining": 0, "quality": 10}]
    update_inventory(items)
    assert items[0] == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}  # 10 - 4 = 6

def test_conjured_item_quality_never_negative():
    items = [{"name": "Conjured Item", "days_remaining": 0, "quality": 3}]
    update_inventory(items)
    assert items[0] == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}  # 3 - 4 = -1 => capped at 0

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10},
    ]
    update_inventory(items)
    assert items == [
        {"name": "Regular Item", "days_remaining": 4, "quality": 9},   # Regular item
        {"name": "Aged Brie", "days_remaining": 4, "quality": 11},     # Aged Brie
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},      # Sulfuras
        {"name": "Backstage Pass", "days_remaining": 14, "quality": 11},  # Backstage Pass
        {"name": "Conjured Item", "days_remaining": 4, "quality": 8},   # Conjured Item
    ]