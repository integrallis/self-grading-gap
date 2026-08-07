# test_gilded_rose.py

from solution import update_inventory

def test_regular_item_quality_decreases_by_1_before_sell_by_date():
    item = {'name': 'Regular Item', 'days_remaining': 5, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 4  # 5 - 1
    assert item['quality'] == 9  # 10 - 1

def test_regular_item_quality_decreases_by_2_after_sell_by_date():
    item = {'name': 'Regular Item', 'days_remaining': 0, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 8  # 10 - 2

def test_regular_item_quality_never_negative():
    item = {'name': 'Regular Item', 'days_remaining': 0, 'quality': 1}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 0  # quality cannot be negative

def test_regular_item_quality_degrades_indefinitely_after_sell_by_date():
    item = {'name': 'Regular Item', 'days_remaining': -1, 'quality': 1}
    update_inventory([item])
    assert item['days_remaining'] == -2  # -1 - 1
    assert item['quality'] == 0  # quality cannot be negative

def test_aged_brie_quality_increases_by_1_before_sell_by_date():
    item = {'name': 'Aged Brie', 'days_remaining': 5, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 4  # 5 - 1
    assert item['quality'] == 11  # 10 + 1

def test_aged_brie_quality_increases_by_2_after_sell_by_date():
    item = {'name': 'Aged Brie', 'days_remaining': 0, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 12  # 10 + 2

def test_aged_brie_quality_never_exceeds_50():
    item = {'name': 'Aged Brie', 'days_remaining': 0, 'quality': 49}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 50  # quality capped at 50

def test_aged_brie_quality_increases_on_final_day():
    item = {'name': 'Aged Brie', 'days_remaining': 1, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 0  # 1 - 1
    assert item['quality'] == 11  # 10 + 1

def test_sulfuras_never_changes():
    item = {'name': 'Sulfuras', 'days_remaining': 0, 'quality': 80}
    update_inventory([item])
    assert item['days_remaining'] == 0  # remains the same
    assert item['quality'] == 80  # remains the same

def test_sulfuras_never_changes_after_sell_by_date():
    item = {'name': 'Sulfuras', 'days_remaining': -1, 'quality': 80}
    update_inventory([item])
    assert item['days_remaining'] == -1  # remains the same
    assert item['quality'] == 80  # remains the same

def test_backstage_pass_quality_increases_by_1_more_than_10_days():
    item = {'name': 'Backstage Pass', 'days_remaining': 15, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 14  # 15 - 1
    assert item['quality'] == 11  # 10 + 1

def test_backstage_pass_quality_increases_by_2_between_10_and_6_days():
    item = {'name': 'Backstage Pass', 'days_remaining': 10, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 9  # 10 - 1
    assert item['quality'] == 12  # 10 + 2

def test_backstage_pass_quality_increases_by_3_between_5_and_1_days():
    item = {'name': 'Backstage Pass', 'days_remaining': 5, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 4  # 5 - 1
    assert item['quality'] == 13  # 10 + 3

def test_backstage_pass_quality_drops_to_0_after_sell_by_date():
    item = {'name': 'Backstage Pass', 'days_remaining': 0, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 0  # drops to 0

def test_backstage_pass_quality_never_exceeds_50():
    item = {'name': 'Backstage Pass', 'days_remaining': 5, 'quality': 49}
    update_inventory([item])
    assert item['days_remaining'] == 4  # 5 - 1
    assert item['quality'] == 50  # quality capped at 50

def test_backstage_pass_quality_remains_0_after_sell_by_date():
    item = {'name': 'Backstage Pass', 'days_remaining': -1, 'quality': 0}
    update_inventory([item])
    assert item['days_remaining'] == -2  # -1 - 1
    assert item['quality'] == 0  # remains at 0

def test_conjured_item_quality_decreases_by_2_before_sell_by_date():
    item = {'name': 'Conjured Item', 'days_remaining': 5, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 4  # 5 - 1
    assert item['quality'] == 8  # 10 - 2

def test_conjured_item_quality_decreases_by_4_after_sell_by_date():
    item = {'name': 'Conjured Item', 'days_remaining': 0, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 6  # 10 - 4

def test_conjured_item_quality_never_negative():
    item = {'name': 'Conjured Item', 'days_remaining': 0, 'quality': 3}
    update_inventory([item])
    assert item['days_remaining'] == -1  # 0 - 1
    assert item['quality'] == 0  # quality cannot be negative

def test_update_inventory_processes_all_items():
    items = [
        {'name': 'Regular Item', 'days_remaining': 5, 'quality': 10},
        {'name': 'Aged Brie', 'days_remaining': 5, 'quality': 10},
        {'name': 'Sulfuras', 'days_remaining': 0, 'quality': 80},
        {'name': 'Backstage Pass', 'days_remaining': 15, 'quality': 10},
        {'name': 'Conjured Item', 'days_remaining': 5, 'quality': 10},
    ]
    update_inventory(items)
    assert items[0]['days_remaining'] == 4 and items[0]['quality'] == 9
    assert items[1]['days_remaining'] == 4 and items[1]['quality'] == 11
    assert items[2]['days_remaining'] == 0 and items[2]['quality'] == 80
    assert items[3]['days_remaining'] == 14 and items[3]['quality'] == 11
    assert items[4]['days_remaining'] == 4 and items[4]['quality'] == 8
    
    # Ensure item names are preserved after update
    assert items[0]['name'] == 'Regular Item'
    assert items[1]['name'] == 'Aged Brie'
    assert items[2]['name'] == 'Sulfuras'
    assert items[3]['name'] == 'Backstage Pass'
    assert items[4]['name'] == 'Conjured Item'
    
def test_backstage_pass_quality_increases_at_boundary_11_days():
    item = {'name': 'Backstage Pass', 'days_remaining': 11, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 10  # 11 - 1
    assert item['quality'] == 11  # 10 + 1

def test_backstage_pass_quality_increases_at_boundary_6_days():
    item = {'name': 'Backstage Pass', 'days_remaining': 6, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 5  # 6 - 1
    assert item['quality'] == 12  # 10 + 2

def test_backstage_pass_quality_increases_at_boundary_1_day():
    item = {'name': 'Backstage Pass', 'days_remaining': 1, 'quality': 10}
    update_inventory([item])
    assert item['days_remaining'] == 0  # 1 - 1
    assert item['quality'] == 13  # 10 + 3