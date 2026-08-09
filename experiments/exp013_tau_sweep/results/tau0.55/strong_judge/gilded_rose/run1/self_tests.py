from solution import update_inventory

def test_regular_item_quality_decreases():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 - 1 = 9
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}

def test_regular_item_quality_decreases_twice_after_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 - 2 = 8
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}

def test_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 1 - 2 = -1 (but should be 0)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}

def test_regular_item_quality_multiple_days_post_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])  # First update
    # Days remaining: -1, Quality: 0 after first update
    update_inventory([item])  # Second update
    # Days remaining: -2, Quality: 0 (should remain 0)
    assert item == {"name": "Regular Item", "days_remaining": -2, "quality": 0}

def test_aged_brie_quality_increases():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}

def test_aged_brie_quality_increases_on_final_day():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # Days remaining: 1 - 1 = 0
    # Quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 0, "quality": 11}

def test_aged_brie_quality_increases_twice_after_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 + 2 = 12
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}

def test_aged_brie_quality_never_exceeds_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 49 + 2 = 51 (but should be capped at 50)
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    # Days remaining: 0 (unchanged)
    # Quality: 80 (unchanged)
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}

def test_sulfuras_remains_unchanged_after_sell_by():
    item = {"name": "Sulfuras", "days_remaining": -1, "quality": 80}
    update_inventory([item])
    # Days remaining: -1 (unchanged)
    # Quality: 80 (unchanged)
    assert item == {"name": "Sulfuras", "days_remaining": -1, "quality": 80}

def test_backstage_pass_quality_increases_with_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 11, "quality": 10}
    update_inventory([item])
    # Days remaining: 11 - 1 = 10
    # Quality: 10 + 1 = 11
    assert item == {"name": "Backstage Pass", "days_remaining": 10, "quality": 11}

def test_backstage_pass_quality_increases_twice_with_10_to_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 10}
    update_inventory([item])
    # Days remaining: 10 - 1 = 9
    # Quality: 10 + 2 = 12
    assert item == {"name": "Backstage Pass", "days_remaining": 9, "quality": 12}

def test_backstage_pass_quality_increases_twice_at_6_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 10}
    update_inventory([item])
    # Days remaining: 6 - 1 = 5
    # Quality: 10 + 2 = 12
    assert item == {"name": "Backstage Pass", "days_remaining": 5, "quality": 12}

def test_backstage_pass_quality_increases_thrice_with_5_to_1_days_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 + 3 = 13
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 13}

def test_backstage_pass_quality_increases_thrice_at_1_day_remaining():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # Days remaining: 1 - 1 = 0
    # Quality: 10 + 3 = 13
    assert item == {"name": "Backstage Pass", "days_remaining": 0, "quality": 13}

def test_backstage_pass_quality_drops_to_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: drops to 0
    assert item == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}

def test_backstage_pass_quality_never_exceeds_50():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 50}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 50 + 3 = 53 (but should be capped at 50)
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 50}

def test_backstage_pass_quality_stays_at_0_after_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 0}
    update_inventory([item])  # First update
    # Days remaining: -1, Quality: 0 (should remain 0)
    update_inventory([item])  # Second update
    # Days remaining: -2, Quality: 0 (should remain 0)
    assert item == {"name": "Backstage Pass", "days_remaining": -2, "quality": 0}

def test_conjured_item_quality_decreases_twice():
    item = {"name": "Conjured", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 - 2 = 8
    assert item == {"name": "Conjured", "days_remaining": 4, "quality": 8}

def test_conjured_item_quality_decreases_four_times_after_sell_by():
    item = {"name": "Conjured", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 - 4 = 6
    assert item == {"name": "Conjured", "days_remaining": -1, "quality": 6}

def test_conjured_item_quality_never_negative():
    item = {"name": "Conjured", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 3 - 4 = -1 (but should be 0)
    assert item == {"name": "Conjured", "days_remaining": -1, "quality": 0}

def test_update_inventory_processes_multiple_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 10},
        {"name": "Conjured", "days_remaining": 5, "quality": 10},
    ]
    update_inventory(items)
    
    # Check each item
    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}
    assert items[1] == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}
    assert items[2] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    assert items[3] == {"name": "Backstage Pass", "days_remaining": 14, "quality": 11}
    assert items[4] == {"name": "Conjured", "days_remaining": 4, "quality": 8}