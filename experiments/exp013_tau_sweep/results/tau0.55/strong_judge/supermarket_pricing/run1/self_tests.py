import pytest
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

def test_different_items():
    # Different items in one basket add their prices together (A with B totals 80).
    assert checkout(['A', 'B']) == 80

def test_multiple_units_no_promotion():
    # Multiple units of an item with no promotion of its own cost the unit price each (two D total 30).
    assert checkout(['D', 'D']) == 30

def test_multi_buy_bundles_A():
    # Three A cost the bundle price of 130 instead of 150.
    assert checkout(['A', 'A', 'A']) == 130

def test_multi_buy_bundles_A_with_extra():
    # Four A total 180 (130 for three A and 50 for the extra A).
    assert checkout(['A', 'A', 'A', 'A']) == 180

def test_multi_buy_bundles_B():
    # Two B cost the bundle price of 45 instead of 60.
    assert checkout(['B', 'B']) == 45

def test_multi_buy_bundles_B_with_extra():
    # Three B total 75 (45 for two B and 30 for the extra B).
    assert checkout(['B', 'B', 'B']) == 75

def test_order_independence():
    # A, B, A, B, A totals 175 in any order.
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175

def test_buy_one_get_one_free_C():
    # Two C total 20 (one is free).
    assert checkout(['C', 'C']) == 20

def test_buy_one_get_one_free_C_with_extra():
    # Three C total 40 (one is free, one is charged).
    assert checkout(['C', 'C', 'C']) == 40

def test_combo_price_D_and_C():
    # One D together with one C costs the combo price of 25.
    assert checkout(['D', 'C']) == 25

def test_combo_price_D_and_C_with_leftovers():
    # D, C and another D total 40 (25 for D and C combo, 15 for the extra D).
    assert checkout(['D', 'C', 'D']) == 40
    # Two D with two C total 50 (25 for each D and C combo).
    assert checkout(['D', 'C', 'D', 'C']) == 50

def test_weighed_goods():
    # Two kilograms of Apples cost 6.98 (3.49 per kilogram).
    assert checkout([('Apples', 2)]) == 6.98

def test_rounding_half_a_kilogram():
    # Half a kilogram of Bananas costs 1.00 (1.99 rounded from 0.995).
    assert checkout([('Bananas', 0.5)]) == 1.00

def test_rounding_one_and_half_kilogram():
    # One and a half kilograms of Bananas costs 2.99 (1.99 * 1.5 rounded).
    assert checkout([('Bananas', 1.5)]) == 2.99

def test_combined_basket():
    # Three A, two B and half a kilogram of Bananas total 176.00.
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00

def test_combined_basket_with_C_BOGO():
    # Two C and half a kilogram of Bananas total 21.00 (20 for C and 1 for Bananas).
    assert checkout(['C', 'C', ('Bananas', 0.5)]) == 21.00

def test_combined_basket_with_D_and_C_combo():
    # D, C and half a kilogram of Bananas total 26.00 (25 for D and C combo, 1 for Bananas).
    assert checkout(['D', 'C', ('Bananas', 0.5)]) == 26.00

def test_unknown_item_scan():
    # Scanning an item that is not in the price list is refused with a message.
    result = checkout(['Grapes'])
    assert result == "Unknown item: Grapes"

def test_unknown_weighed_item_scan():
    # Weighing an item that is not in the price list is refused with the same message.
    result = checkout([('Grapes', 1)])
    assert result == "Unknown item: Grapes"

def test_negative_weight():
    # A weighed item's weight must be positive; zero or negative weight is refused.
    result = checkout([('Bananas', 0)])
    assert result == "weight must be positive"
    result = checkout([('Bananas', -1)])
    assert result == "weight must be positive"

def test_rounding_two_weighed_lines():
    # Two separately rounded weighed lines total 2.00 (1.00 each).
    assert checkout([('Bananas', 0.5), ('Bananas', 0.5)]) == 2.00