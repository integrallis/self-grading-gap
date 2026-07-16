# test_gilded_rose.py

from solution import update_inventory

def test_regular_item_degrades_quality_and_days():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 - 1 = 9
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}

def test_regular_item_quality_doubles_after_sell_by_date():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 - 2 = 8
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 1 - 2 = -1 (but should be 0)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}

def test_aged_brie_increases_quality_before_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}

def test_aged_brie_increases_quality_after_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 + 2 = 12
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 49 + 2 = 51 (but should be 50)
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    # days_remaining: 0 remains 0
    # quality: 80 remains 80
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}

def test_backstage_pass_quality_increases_with_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 15, "quality": 10}
    update_inventory([item])
    # days_remaining: 15 - 1 = 14
    # quality: 10 + 1 = 11
    assert item == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}

def test_backstage_pass_quality_increases_2_with_10_to_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    # days_remaining: 10 - 1 = 9
    # quality: 10 + 2 = 12
    assert item == {"name": "Backstage Pass", "days_remaining": 9, "quality": 12}

def test_backstage_pass_quality_increases_3_with_5_to_1_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 + 3 = 13
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 13}

def test_backstage_pass_quality_drops_to_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 drops to 0
    assert item == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 49}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 49 + 3 = 52 (but should be 50)
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 50}

def test_conjured_item_degrades_quality_twice_as_fast():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 - 2 = 8
    assert item == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}

def test_conjured_item_degrades_quality_twice_as_fast_after_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 - 4 = 6
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 3 - 4 = -1 (but should be 0)
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}

def test_update_inventory_processes_multiple_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)

    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}
    assert items[1] == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}
    assert items[2] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    assert items[3] == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}
    assert items[4] == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}