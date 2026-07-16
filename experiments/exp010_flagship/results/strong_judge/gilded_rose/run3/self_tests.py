# test_gilded_rose.py

from solution import update_inventory

def test_regular_item_degrades_quality_and_days():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}  # Quality decreases by 1

def test_regular_item_degrades_quality_twice_after_sell_by_date():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}  # Quality decreases by 2

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}  # Quality cannot go below 0

def test_regular_item_doubles_degradation_indefinitely():
    item = {"name": "Regular Item", "days_remaining": -1, "quality": 5}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -2, "quality": 3}  # Quality decreases by 2

def test_aged_brie_gains_quality_before_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 2, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": 1, "quality": 11}  # Quality increases by 1

def test_aged_brie_gains_quality_on_final_pre_expiry_day():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": 0, "quality": 11}  # Quality increases by 1

def test_aged_brie_gains_quality_after_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}  # Quality increases by 2

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}  # Quality cannot exceed 50

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}  # No changes at all

def test_backstage_pass_quality_increases_with_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 15, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}  # Quality increases by 1

def test_backstage_pass_quality_increases_by_1_at_11_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 10, "quality": 11}  # Quality increases by 1

def test_backstage_pass_quality_increases_by_2_with_10_to_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 9, "quality": 12}  # Quality increases by 2

def test_backstage_pass_quality_increases_by_2_at_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 5, "quality": 12}  # Quality increases by 2

def test_backstage_pass_quality_increases_by_3_with_5_to_1_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 13}  # Quality increases by 3

def test_backstage_pass_quality_increases_by_3_at_1_day_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 0, "quality": 13}  # Quality increases by 3

def test_backstage_pass_quality_drops_to_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}  # Quality drops to 0

def test_backstage_pass_quality_stays_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": -2, "quality": 0}  # Quality remains 0

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 49}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 0, "quality": 50}  # Quality cannot exceed 50

def test_conjured_item_degrades_quality_doubly_fast_before_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}  # Quality decreases by 2

def test_conjured_item_degrades_quality_doubly_fast_after_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}  # Quality decreases by 4

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}  # Quality cannot go below 0

def test_update_inventory_processes_multiple_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 2, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)
    assert items == [
        {"name": "Regular Item", "days_remaining": 4, "quality": 9},
        {"name": "Aged Brie", "days_remaining": 1, "quality": 11},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 14, "quality": 11},
        {"name": "Conjured Item", "days_remaining": 4, "quality": 8}
    ]  # All items updated correctly