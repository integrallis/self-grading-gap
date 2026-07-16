from solution import checkout

def test_empty_basket():
    assert checkout([]) == 0  # AC-1.1: An empty basket totals 0.

def test_single_item_prices():
    assert checkout(['A']) == 50  # AC-1.2: Unit price A costs 50.
    assert checkout(['B']) == 30  # AC-1.2: Unit price B costs 30.
    assert checkout(['C']) == 20  # AC-1.2: Unit price C costs 20.
    assert checkout(['D']) == 15  # AC-1.2: Unit price D costs 15.

def test_different_items():
    assert checkout(['A', 'B']) == 80  # AC-1.3: A (50) + B (30) = 80.
    assert checkout(['C', 'D']) == 35  # AC-1.3: C (20) + D (15) = 35.

def test_multiple_units_no_promotion():
    assert checkout(['D', 'D']) == 30  # AC-1.4: 2 D (15 each) = 30.

def test_multi_buy_bundles_A():
    assert checkout(['A', 'A', 'A']) == 130  # AC-2.1: 3 A cost bundle price 130.
    assert checkout(['A', 'A', 'A', 'A']) == 180  # AC-2.2: 4 A (130 + 50) = 180.

def test_multi_buy_bundles_B():
    assert checkout(['B', 'B']) == 45  # AC-2.3: 2 B cost bundle price 45.
    assert checkout(['B', 'B', 'B']) == 75  # AC-2.4: 3 B (45 + 30) = 75.

def test_order_independence():
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # AC-2.5: Any order totals 175.
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175  # AC-2.5: Any order totals 175.

def test_buy_one_get_one_free_C():
    assert checkout(['C', 'C']) == 20  # AC-3.1: 2 C (20 total).
    assert checkout(['C', 'C', 'C']) == 40  # AC-3.2: 3 C (20 + 20).

def test_combo_price_D_and_C():
    assert checkout(['D', 'C']) == 25  # AC-4.1: D (15) + C (20) = 25 for combo.
    assert checkout(['D', 'C', 'D']) == 40  # AC-4.2: D, C and another D = 40.
    assert checkout(['D', 'C', 'D', 'C']) == 50  # AC-4.2: 2 D with 2 C = 50.

def test_weighed_goods():
    assert checkout([('Bananas', 1)]) == 1.99  # AC-5.1: Bananas 1 kg = 1.99.
    assert checkout([('Apples', 2)]) == 6.98  # AC-5.1: 2 kg of Apples = 6.98.
    
    assert checkout([('Bananas', 0.5)]) == 1.00  # AC-5.2: 0.5 kg of Bananas = 1.00.
    assert checkout([('Bananas', 1.5)]) == 2.99  # AC-5.2: 1.5 kg of Bananas = 2.99.

def test_combined_basket():
    assert checkout(['A', 'A', 'B', 'C', ('Bananas', 0.5)]) == 176.00  # AC-5.3: 3 A + 2 B + 0.5 kg Bananas.

def test_invalid_scans():
    assert checkout(['E']) == "Unknown item: E"  # AC-6.1: Unknown item.
    assert checkout([('Grapes', 1)]) == "Unknown item: Grapes"  # AC-6.2: Unknown item.
    assert checkout([('Bananas', 0)]) == "weight must be positive"  # AC-6.3: Non-positive weight.
    assert checkout([('Bananas', -1)]) == "weight must be positive"  # AC-6.3: Non-positive weight.