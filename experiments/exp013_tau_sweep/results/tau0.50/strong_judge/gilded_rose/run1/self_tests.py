from solution import update_inventory

def test_age_regular_item():
    item = {"name": "Regular Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": 4, "quality": 9}  # 1 day down, 1 quality down

def test_age_regular_item_passed_sell_by_date():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 8}  # 1 day down, 2 quality down

def test_age_regular_item_quality_never_negative():
    item = {"name": "Regular Item", "days_remaining": 0, "quality": 1}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -1, "quality": 0}  # 1 day down, 2 quality down but can't go below 0

def test_age_regular_item_indefinitely_after_expiry():
    item = {"name": "Regular Item", "days_remaining": -1, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Regular Item", "days_remaining": -2, "quality": 8}  # 1 day down, 2 quality down

def test_age_aged_brie():
    item = {"name": "Aged Brie", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}  # 1 day down, 1 quality up

def test_age_aged_brie_quality_max():
    item = {"name": "Aged Brie", "days_remaining": 1, "quality": 50}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": 0, "quality": 50}  # 1 day down, can't exceed 50

def test_age_aged_brie_passed_sell_by_date():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 12}  # 1 day down, 2 quality up

def test_age_aged_brie_expired_cap():
    item = {"name": "Aged Brie", "days_remaining": 0, "quality": 49}
    update_inventory([item])
    assert item == {"name": "Aged Brie", "days_remaining": -1, "quality": 50}  # 1 day down, 2 quality up but capped at 50

def test_age_sulfuras():
    item = {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    update_inventory([item])
    assert item == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}  # No change

def test_age_sulfuras_passed_sell_by_date():
    item = {"name": "Sulfuras", "days_remaining": -1, "quality": 80}
    update_inventory([item])
    assert item == {"name": "Sulfuras", "days_remaining": -1, "quality": 80}  # No change after expiry

def test_age_backstage_pass():
    item = {"name": "Backstage Pass", "days_remaining": 15, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 14, "quality": 21}  # 1 day down, 1 quality up

def test_age_backstage_pass_10_days():
    item = {"name": "Backstage Pass", "days_remaining": 10, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 9, "quality": 22}  # 1 day down, 2 quality up

def test_age_backstage_pass_6_days():
    item = {"name": "Backstage Pass", "days_remaining": 6, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 5, "quality": 22}  # 1 day down, 2 quality up

def test_age_backstage_pass_5_days():
    item = {"name": "Backstage Pass", "days_remaining": 5, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 4, "quality": 23}  # 1 day down, 3 quality up

def test_age_backstage_pass_1_day():
    item = {"name": "Backstage Pass", "days_remaining": 1, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": 0, "quality": 23}  # 1 day down, 3 quality up

def test_age_backstage_pass_passed_concert():
    item = {"name": "Backstage Pass", "days_remaining": 0, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": -1, "quality": 0}  # 1 day down, drops to 0

def test_age_backstage_pass_already_passed_concert():
    item = {"name": "Backstage Pass", "days_remaining": -1, "quality": 20}
    update_inventory([item])
    assert item == {"name": "Backstage Pass", "days_remaining": -2, "quality": 0}  # No change, stays at 0

def test_age_conjured_item():
    item = {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}  # 1 day down, 2 quality down

def test_age_conjured_item_passed_sell_by_date():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 6}  # 1 day down, 4 quality down

def test_age_conjured_item_quality_never_negative():
    item = {"name": "Conjured Item", "days_remaining": 0, "quality": 3}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": -1, "quality": 0}  # 1 day down, 4 quality down but can't go below 0

def test_age_conjured_item_indefinitely_after_expiry():
    item = {"name": "Conjured Item", "days_remaining": -1, "quality": 10}
    update_inventory([item])
    assert item == {"name": "Conjured Item", "days_remaining": -2, "quality": 6}  # 1 day down, 4 quality down

def test_update_inventory_processes_all_items():
    items = [
        {"name": "Regular Item", "days_remaining": 5, "quality": 10},
        {"name": "Aged Brie", "days_remaining": 5, "quality": 10},
        {"name": "Sulfuras", "days_remaining": 0, "quality": 80},
        {"name": "Backstage Pass", "days_remaining": 15, "quality": 20},
        {"name": "Conjured Item", "days_remaining": 5, "quality": 10}
    ]
    update_inventory(items)
    assert items[0] == {"name": "Regular Item", "days_remaining": 4, "quality": 9}
    assert items[1] == {"name": "Aged Brie", "days_remaining": 4, "quality": 11}
    assert items[2] == {"name": "Sulfuras", "days_remaining": 0, "quality": 80}
    assert items[3] == {"name": "Backstage Pass", "days_remaining": 14, "quality": 21}
    assert items[4] == {"name": "Conjured Item", "days_remaining": 4, "quality": 8}