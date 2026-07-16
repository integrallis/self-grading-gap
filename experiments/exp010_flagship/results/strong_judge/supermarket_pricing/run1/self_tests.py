from solution import checkout

def test_empty_basket_totals_zero():
    assert checkout([]) == 0  # An empty basket totals 0.

def test_unit_prices():
    assert checkout(['A']) == 50  # Unit price for A is 50.
    assert checkout(['B']) == 30  # Unit price for B is 30.
    assert checkout(['C']) == 20  # Unit price for C is 20.
    assert checkout(['D']) == 15  # Unit price for D is 15.

def test_different_items_in_one_basket():
    assert checkout(['A', 'B']) == 80  # A (50) + B (30) = 80.
    
def test_multiple_units_of_item_without_promotion():
    assert checkout(['D', 'D']) == 30  # 2 * D (15) = 30.

def test_bundle_deal_for_A():
    assert checkout(['A', 'A', 'A']) == 130  # 3 * A costs 130 instead of 150.
    assert checkout(['A', 'A', 'A', 'A']) == 180  # 4 * A costs 180 (130 + 50).

def test_bundle_deal_for_B():
    assert checkout(['B', 'B']) == 45  # 2 * B costs 45 instead of 60.
    assert checkout(['B', 'B', 'B']) == 75  # 3 * B costs 75 (45 + 30).

def test_total_order_invariance():
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # 3A (130) + 2B (45).
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175  # Same items in different order.

def test_buy_one_get_one_free_for_C():
    assert checkout(['C', 'C']) == 20  # 2 * C costs 20.
    assert checkout(['C', 'C', 'C']) == 40  # 3 * C costs 40.

def test_combo_price_for_D_and_C():
    assert checkout(['D', 'C']) == 25  # D (15) + C (20) = 25.
    assert checkout(['D', 'C', 'D']) == 40  # D (15) + C (20) + D (15) = 40.
    assert checkout(['D', 'C', 'D', 'C']) == 50  # 2D (30) + 2C (20) = 50.

def test_weighted_goods_pricing():
    assert checkout([('Bananas', 1)]) == 1.99  # 1 * Bananas (1.99).
    assert checkout([('Apples', 2)]) == 6.98  # 2 * Apples (3.49 each) = 6.98.
    assert checkout([('Bananas', 0.5)]) == 1.00  # 0.5 * Bananas (1.99) = round(0.995) = 1.00.
    assert checkout([('Bananas', 1.5)]) == 2.99  # 1.5 * Bananas (1.99) = round(2.985) = 2.99.

def test_combined_basket_with_weighted_goods():
    assert checkout(['A', 'A', 'C', ('Bananas', 0.5)]) == 121.00  # 2A (100) + C (20) + Bananas (1.00) = 121.00.
    assert checkout([('Bananas', 0.5), 'A', 'A', 'C']) == 121.00  # Same items in different order.
    assert checkout(['A', 'A', ('Bananas', 0.5), 'B', 'B']) == 176.00  # 3A (130) + 2B (45) + Bananas (1.00) = 176.00.

def test_unknown_item_scan():
    assert checkout(['X']) == "Unknown item: X"  # Invalid item 'X'.
    assert checkout([('Grapes', 1)]) == "Unknown item: Grapes"  # Invalid weighed item 'Grapes'.

def test_zero_or_negative_weight():
    assert checkout([('Bananas', 0)]) == "weight must be positive"  # Zero weight error.
    assert checkout([('Bananas', -1)]) == "weight must be positive"  # Negative weight error.