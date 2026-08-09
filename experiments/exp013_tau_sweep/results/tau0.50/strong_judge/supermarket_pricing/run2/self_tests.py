import pytest
from solution import checkout

def test_empty_basket():
    # An empty basket totals 0
    assert checkout([]) == 0

def test_unit_prices():
    # Unit prices are: A costs 50, B costs 30, C costs 20, D costs 15.
    assert checkout(['A']) == 50
    assert checkout(['B']) == 30
    assert checkout(['C']) == 20
    assert checkout(['D']) == 15

def test_multiple_items():
    # Different items in one basket add their prices together (A with B totals 80).
    assert checkout(['A', 'B']) == 80

def test_multiple_units_no_promotion():
    # Two D total 30 (two D cost 15 each).
    assert checkout(['D', 'D']) == 30

def test_bundle_deals_A():
    # Three A cost the bundle price of 130 instead of 150 (3 * 50 - 20).
    assert checkout(['A', 'A', 'A']) == 130
    # Four A total 180 (3 for 130 plus 1 at unit price 50).
    assert checkout(['A', 'A', 'A', 'A']) == 180

def test_bundle_deals_B():
    # Two B cost the bundle price of 45 instead of 60 (2 * 30 - 15).
    assert checkout(['B', 'B']) == 45
    # Three B total 75 (2 for 45 plus 1 at unit price 30).
    assert checkout(['B', 'B', 'B']) == 75

def test_order_independence():
    # A, B, A, B, A totals 175 (3 A for 130, 2 B for 45).
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175
    # C, D totals the combo price of 25 (order independence).
    assert checkout(['C', 'D']) == 25
    assert checkout(['D', 'C']) == 25

def test_buy_one_get_one_free_C():
    # Two C total 20 (1 C at 20 and 1 free).
    assert checkout(['C', 'C']) == 20
    # Three C total 40 (2 C at 20 and 1 at unit price 20).
    assert checkout(['C', 'C', 'C']) == 40

def test_combo_price_D_and_C():
    # One D together with one C costs the combo price of 25.
    assert checkout(['D', 'C']) == 25
    # D, C and another D total 40 (1 combo price of 25 and 1 D at 15).
    assert checkout(['D', 'C', 'D']) == 40
    # Two D with two C total 50 (2 combos of 25).
    assert checkout(['D', 'C', 'D', 'C']) == 50

def test_produce_pricing():
    # Two kilograms of Apples cost 6.98 (2 * 3.49).
    assert checkout([('Apples', 2)]) == 6.98
    # Half a kilogram of Bananas comes to 1.00 (1.99/2).
    assert checkout([('Bananas', 0.5)]) == 1.00
    # One and a half kilograms of Bananas comes to 2.99 (1.99 + 1.99/2).
    assert checkout([('Bananas', 1.5)]) == 2.99
    # Three A, two B and half a kilogram of Bananas total 176.00.
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00

def test_invalid_item_scan():
    # Scanning an item that is not in the price list is refused.
    with pytest.raises(Exception) as exc:
        checkout(['X'])
    assert str(exc.value) == "Unknown item: X"

def test_invalid_weighing_item_scan():
    # Weighing an item that is not in the price list is refused.
    with pytest.raises(Exception) as exc:
        checkout([('Grapes', 1)])
    assert str(exc.value) == "Unknown item: Grapes"

def test_negative_weight():
    # A weighed item's weight must be positive; zero or negative weight is refused.
    with pytest.raises(Exception) as exc:
        checkout([('Apples', 0)])
    assert str(exc.value) == "weight must be positive"
    
    with pytest.raises(Exception) as exc:
        checkout([('Bananas', -1)])
    assert str(exc.value) == "weight must be positive"

def test_weighed_line_rounding():
    # Two separate 0.5 kg Banana lines totaling 2.00 instead of 1.99.
    assert checkout([('Bananas', 0.5)]) == 1.00
    assert checkout([('Bananas', 0.5)]) == 1.00
    assert checkout([('Bananas', 0.5), ('Bananas', 0.5)]) == 2.00