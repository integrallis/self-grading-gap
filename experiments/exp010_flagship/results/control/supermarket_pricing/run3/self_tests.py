from solution import checkout

def test_empty_basket():
    # AC-1.1: An empty basket totals 0.
    assert checkout([]) == 0

def test_single_item():
    # AC-1.2: Unit prices are: A costs 50, B costs 30, C costs 20, D costs 15.
    assert checkout(['A']) == 50
    assert checkout(['B']) == 30
    assert checkout(['C']) == 20
    assert checkout(['D']) == 15

def test_multiple_items():
    # AC-1.3: Different items in one basket add their prices together (A with B totals 80).
    assert checkout(['A', 'B']) == 80
    # AC-1.4: Multiple units of an item with no promotion of its own cost the unit price each (two D total 30).
    assert checkout(['D', 'D']) == 30

def test_bundle_deals():
    # AC-2.1: Three A cost the bundle price of 130 instead of 150.
    assert checkout(['A', 'A', 'A']) == 130
    # AC-2.2: Units of A beyond a complete bundle are charged at unit price (four A total 180).
    assert checkout(['A', 'A', 'A', 'A']) == 180
    # AC-2.3: Two B cost the bundle price of 45 instead of 60.
    assert checkout(['B', 'B']) == 45
    # AC-2.4: Units of B beyond a complete bundle are charged at unit price (three B total 75).
    assert checkout(['B', 'B', 'B']) == 75
    # AC-2.5: The total never depends on the order in which items are scanned (A, B, A, B, A totals 175 in any order).
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175

def test_buy_one_get_one_free():
    # AC-3.1: Every second C in the basket is free (two C total 20).
    assert checkout(['C', 'C']) == 20
    # AC-3.2: An unpaired C is charged at unit price (three C total 40).
    assert checkout(['C', 'C', 'C']) == 40

def test_combo_deals():
    # AC-4.1: One D together with one C costs the combo price of 25.
    assert checkout(['D', 'C']) == 25
    # AC-4.2: The combo applies once per disjoint D-and-C pair; leftovers are charged at unit price (D, C and another D total 40; two D with two C total 50).
    assert checkout(['D', 'C', 'D']) == 40
    assert checkout(['D', 'D', 'C', 'C']) == 50

def test_weighted_goods():
    # AC-5.1: Weighed goods are priced per kilogram: Bananas at 1.99, Apples at 3.49 (two kilograms of Apples cost 6.98).
    assert checkout(['Bananas', 1]) == 1.99
    assert checkout(['Apples', 2]) == 6.98
    # AC-5.2: Each weighed line is rounded to the nearest cent, with exact halves rounding up.
    assert checkout(['Bananas', 0.5]) == 1.00  # 0.995 rounded up
    assert checkout(['Bananas', 1.5]) == 2.99  # 2.985 rounded up
    # AC-5.3: Weighed lines combine with all other pricing rules in a single basket.
    assert checkout(['A', 'A', 'A', 'B', 'B', 'Bananas', 0.5]) == 211.00  # 150 + 60 + 1 = 211

def test_invalid_scans():
    # AC-6.1: Scanning an item that is not in the price list is refused with a message naming the item.
    assert checkout(['X']) == "Unknown item: X"
    
    # AC-6.2: Weighing an item that is not in the price list is refused the same way.
    assert checkout(['Grapes', 1]) == "Unknown item: Grapes"
    
    # AC-6.3: A weighed item's weight must be positive; zero or negative weight is refused.
    assert checkout(['Bananas', 0]) == "weight must be positive"
    assert checkout(['Bananas', -1]) == "weight must be positive"