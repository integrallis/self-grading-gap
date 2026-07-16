from solution import update_inventory

def test_regular_item_degrades():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 - 1 = 9
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}

def test_regular_item_degrades_twice_after_sell_by():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 - 2 = 8 (degrades twice after sell-by)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}

def test_regular_item_quality_does_not_go_below_zero():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 1 - 2 = -1 (should not go below 0)
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}

def test_aged_brie_increases_quality_before_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 10}
    update_inventory([item])
    # Days remaining: 1 - 1 = 0
    # Quality: 10 + 1 = 11
    assert item == {"name": "Aged Brie", "days_remaining": 0, "quality": 11}

def test_aged_brie_increases_quality_after_sell_by():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 + 2 = 12
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}

def test_aged_brie_quality_does_not_exceed_50():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 49 + 2 = 51 (should not exceed 50)
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}

def test_sulfuras_never_changes():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    # Days remaining: remains 0
    # Quality: remains 80
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}

def test_backstage_passes_quality_increases():
    item = {"name": "Backstage passes", "days_remaining": 12, "quality": 10}
    update_inventory([item])
    # Days remaining: 12 - 1 = 11
    # Quality: 10 + 1 = 11
    assert item == {"name": "Backstage passes", "days_remaining": 11, "quality": 11}

def test_backstage_passes_quality_increases_twice():
    item = {"name": "Backstage passes", "days_remaining": 8, "quality": 10}
    update_inventory([item])
    # Days remaining: 8 - 1 = 7
    # Quality: 10 + 2 = 12
    assert item == {"name": "Backstage passes", "days_remaining": 7, "quality": 12}

def test_backstage_passes_quality_increases_thrice():
    item = {"name": "Backstage passes", "days_remaining": 4, "quality": 10}
    update_inventory([item])
    # Days remaining: 4 - 1 = 3
    # Quality: 10 + 3 = 13
    assert item == {"name": "Backstage passes", "days_remaining": 3, "quality": 13}

def test_backstage_passes_quality_drops_to_zero_after_concert():
    item = {"name": "Backstage passes", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: drops to 0
    assert item == {"name": "Backstage passes", "days_remaining": -1, "quality": 0}

def test_backstage_passes_quality_does_not_exceed_50():
    item = {"name": "Backstage passes", "days_remaining": 4, "quality": 49}
    update_inventory([item])
    # Days remaining: 4 - 1 = 3
    # Quality: 49 + 3 = 52 (should not exceed 50)
    assert item == {"name": "Backstage passes", "days_remaining": 3, "quality": 50}

def test_conjured_item_degrades_twice():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    # Days remaining: 5 - 1 = 4
    # Quality: 10 - 2 = 8
    assert item == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}

def test_conjured_item_degrades_four_times_after_sell_by():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 10 - 4 = 6
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}

def test_conjured_item_quality_does_not_go_below_zero():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    # Days remaining: 0 - 1 = -1
    # Quality: 3 - 4 = -1 (should not go below 0)
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 1, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage passes", "days_remaining": 12, "quality": 10},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10},
    ]
    update_inventory(items)
    
    # Checking all items after update
    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}
    assert items[1] == {"name": "Aged Brie", "days_remaining": 0, "quality": 11}
    assert items[2] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    assert items[3] == {"name": "Backstage passes", "days_remaining": 11, "quality": 11}
    assert items[4] == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}