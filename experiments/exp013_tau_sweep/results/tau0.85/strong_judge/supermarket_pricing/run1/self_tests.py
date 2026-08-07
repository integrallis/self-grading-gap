from solution import checkout

def test_empty_basket():
    # An empty basket totals 0.
    assert checkout([]) == 0

def test_unit_prices():
    # Unit prices are: A costs 50, B costs 30, C costs 20, D costs 15.
    assert checkout(['A']) == 50
    assert checkout(['B']) == 30
    assert checkout(['C']) == 20
    assert checkout(['D']) == 15
    # Different items in one basket add their prices together (A with B totals 80).
    assert checkout(['A', 'B']) == 80
    # Multiple units of an item with no promotion of its own cost the unit price each (two D total 30).
    assert checkout(['D', 'D']) == 30

def test_multi_buy_bundles():
    # Three A cost the bundle price of 130 instead of 150.
    assert checkout(['A', 'A', 'A']) == 130
    # Four A total 180 (three at bundle price and one at unit price).
    assert checkout(['A', 'A', 'A', 'A']) == 180
    # Two B cost the bundle price of 45 instead of 60.
    assert checkout(['B', 'B']) == 45
    # Three B total 75 (two at bundle price and one at unit price).
    assert checkout(['B', 'B', 'B']) == 75
    # The total never depends on the order in which items are scanned (A, B, A, B, A totals 175 in any order).
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175
    assert checkout(['A', 'A', 'B', 'A', 'B']) == 175
    assert checkout(['B', 'A', 'A', 'B', 'A']) == 175

def test_buy_one_get_one_free():
    # Every second C in the basket is free (two C total 20).
    assert checkout(['C', 'C']) == 20
    # An unpaired C is charged at unit price (three C total 40).
    assert checkout(['C', 'C', 'C']) == 40

def test_combo_price():
    # One D together with one C costs the combo price of 25.
    assert checkout(['D', 'C']) == 25
    # D, C and another D total 40 (one combo price and one D at unit price).
    assert checkout(['D', 'C', 'D']) == 40
    # Two D with two C total 50 (two combo prices).
    assert checkout(['D', 'C', 'D', 'C']) == 50
    # Order independence for D-C combo (C, D, C, D totals 50).
    assert checkout(['C', 'D', 'C', 'D']) == 50

def test_produce_by_weight():
    # Weighed goods are priced per kilogram: Bananas at 1.99, Apples at 3.49 (two kilograms of Apples cost 6.98).
    assert checkout(['Bananas', 1]) == 1.99
    assert checkout(['Apples', 2]) == 6.98
    # Half a kilogram of Bananas comes to 0.995 and is charged as 1.00.
    assert checkout(['Bananas', 0.5]) == 1.00
    # One and a half kilograms comes to 2.985 and is charged as 2.99.
    assert checkout(['Bananas', 1.5]) == 2.99
    # Two half-kilogram Banana lines total 2.00 rather than aggregating to 1.99.
    assert checkout(['Bananas', 0.5]) == 1.00
    assert checkout(['Bananas', 0.5]) == 1.00
    assert checkout(['Bananas', 0.5, 'Bananas', 0.5]) == 2.00
    # Three A, two B and half a kilogram of Bananas total 176.00.
    assert checkout(['A', 'A', 'A', 'B', 'B', 'Bananas', 0.5]) == 176.00

def test_refuse_bad_scans():
    # Scanning an item that is not in the price list is refused with a message naming the item.
    assert checkout(['X']) == "Unknown item: X"
    # Weighing an item that is not in the price list is refused the same way.
    assert checkout(['Grapes', 1]) == "Unknown item: Grapes"
    # A weighed item's weight must be positive; zero or negative weight is refused with the message exactly "weight must be positive".
    assert checkout(['Bananas', 0]) == "weight must be positive"
    assert checkout(['Bananas', -1]) == "weight must be positive"