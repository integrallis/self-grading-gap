# your complete test file
from solution import update_inventory

def test_regular_item_before_sell_by():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 - 1 = 9
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}

def test_regular_item_after_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 - 2 = 8 (degrades twice as fast)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 1 - 2 = -1 (but should not go below 0)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}

def test_regular_item_repeated_update_post_date():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    update_inventory([item])
    # After first update: days_remaining = -1, quality = 8
    # After second update: days_remaining = -2, quality = 6 (8 - 2)
    assert item == {"name": "Regular Item", "days_remaining": -2, "quality": 6}

def test_aged_brie_before_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}

def test_aged_brie_on_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 + 2 = 12
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 49 + 2 = 51 (but should not exceed 50)
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}

def test_aged_brie_on_final_day():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # days_remaining: 1 - 1 = 0
    # quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 0, "quality": 11}

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    # days_remaining: 0 (remains 0)
    # quality: 80 (remains 80)
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}

def test_sulfuras_with_negative_days():
    item = {"name": "Sulfuras", "days_remaining": -1, "quality": 80}
    update_inventory([item])
    # days_remaining: -1 (remains -1)
    # quality: 80 (remains 80)
    assert item == {"name": "Sulfuras", "days_remaining": -1, "quality": 80}

def test_backstage_pass_more_than_10_days():
    item = {"name": "Backstage Pass", "days_remaining": 15, "quality": 10}
    update_inventory([item])
    # days_remaining: 15 - 1 = 14
    # quality: 10 + 1 = 11
    assert item == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}

def test_backstage_pass_at_11_days():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    # days_remaining: 11 - 1 = 10
    # quality: 10 + 1 = 11
    assert item == {"name": "Backstage Pass", "days_remaining": 10, "quality": 11}

def test_backstage_pass_between_10_and_6_days():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    # days_remaining: 10 - 1 = 9
    # quality: 10 + 2 = 12
    assert item == {"name": "Backstage Pass", "days_remaining": 9, "quality": 12}

def test_backstage_pass_at_6_days():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 10}
    update_inventory([item])
    # days_remaining: 6 - 1 = 5
    # quality: 10 + 2 = 12
    assert item == {"name": "Backstage Pass", "days_remaining": 5, "quality": 12}

def test_backstage_pass_between_5_and_1_days():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 + 3 = 13
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 13}

def test_backstage_pass_at_1_day():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # days_remaining: 1 - 1 = 0
    # quality: 10 + 3 = 13
    assert item == {"name": "Backstage Pass", "days_remaining": 0, "quality": 13}

def test_backstage_pass_after_sell_by():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 0 (drops to 0)
    assert item == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 48}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 48 + 3 = 51 (but should not exceed 50)
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 50}

def test_backstage_pass_repeated_update_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    update_inventory([item])
    # After first update: days_remaining = -1, quality = 0
    # After second update: days_remaining = -2, quality = 0 (stays at 0)
    assert item == {"name": "Backstage Pass", "days_remaining": -2, "quality": 0}

def test_conjured_item_before_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # days_remaining: 5 - 1 = 4
    # quality: 10 - 2 = 8
    assert item == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}

def test_conjured_item_after_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 10 - 4 = 6
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    # days_remaining: 0 - 1 = -1
    # quality: 3 - 4 = -1 (but should not go below 0)
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)
    # Check regular item
    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}
    # Check Aged Brie
    assert items[1] == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}
    # Check Sulfuras
    assert items[2] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    # Check Backstage Pass
    assert items[3] == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}
    # Check Conjured Item
    assert items[4] == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}