# test_supermarket_checkout.py

def test_empty_basket_totals_zero():
    assert checkout([]) == 0  # An empty basket totals 0.

def test_unit_prices():
    assert checkout(['A']) == 50  # A costs 50.
    assert checkout(['B']) == 30  # B costs 30.
    assert checkout(['C']) == 20  # C costs 20.
    assert checkout(['D']) == 15  # D costs 15.
    assert checkout(['A', 'B']) == 80  # A (50) + B (30) = 80.
    assert checkout(['D', 'D']) == 30  # 2 D (15 each) = 30.

def test_multi_buy_bundles():
    assert checkout(['A', 'A', 'A']) == 130  # 3 A cost 130 instead of 150.
    assert checkout(['A', 'A', 'A', 'A']) == 180  # 4 A cost 180 (130 + 50).
    assert checkout(['B', 'B']) == 45  # 2 B cost 45 instead of 60.
    assert checkout(['B', 'B', 'B']) == 75  # 3 B cost 75 (45 + 30).
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # A, B, A, B, A totals 175.
    assert checkout(['B', 'A', 'A', 'B', 'A']) == 175  # Order independence test.

def test_buy_one_get_one_free():
    assert checkout(['C', 'C']) == 20  # 2 C total 20 (1 paid, 1 free).
    assert checkout(['C', 'C', 'C']) == 40  # 3 C total 40 (2 paid, 1 free).

def test_combo_price_for_d_and_c():
    assert checkout(['D', 'C']) == 25  # D (15) + C (20) = combo price of 25.
    assert checkout(['D', 'C', 'D']) == 40  # D, C, and another D total 40 (25 + 15).
    assert checkout(['D', 'D', 'C', 'C']) == 50  # 2 D with 2 C total 50 (25 + 25).

def test_weighed_goods():
    assert checkout([('Bananas', 1)]) == 1.99  # 1 kg of Bananas costs 1.99.
    assert checkout([('Apples', 2)]) == 6.98  # 2 kg of Apples costs 6.98 (3.49 * 2).
    assert checkout([('Bananas', 0.5)]) == 1.00  # 0.5 kg of Bananas costs 1.00 (rounding up).
    assert checkout([('Bananas', 1.5)]) == 2.99  # 1.5 kg of Bananas costs 2.99 (rounding up).
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00  # 3 A (130) + 2 B (45) + 1.00 = 176.00.

def test_unknown_item_scan():
    assert checkout(['Grapes']) == "Unknown item: Grapes"  # Unknown item error.
    assert checkout([('Grapes', 1)]) == "Unknown item: Grapes"  # Unknown item error on weight.

def test_negative_or_zero_weight():
    assert checkout([('Bananas', 0)]) == "weight must be positive"  # Zero weight error.
    assert checkout([('Bananas', -1)]) == "weight must be positive"  # Negative weight error.