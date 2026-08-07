import pytest
from solution import checkout

def test_empty_basket_totals_zero():
    # An empty basket should total 0.
    assert checkout([]) == 0

def test_unit_prices():
    # Unit prices are: A costs 50, B costs 30, C costs 20, D costs 15.
    assert checkout(['A']) == 50
    assert checkout(['B']) == 30
    assert checkout(['C']) == 20
    assert checkout(['D']) == 15

def test_different_items_add_prices():
    # A with B totals 80.
    assert checkout(['A', 'B']) == 80

def test_multiple_units_no_promotion():
    # Two D total 30.
    assert checkout(['D', 'D']) == 30

def test_bundle_price_for_A():
    # Three A cost the bundle price of 130 instead of 150.
    assert checkout(['A', 'A', 'A']) == 130

def test_bundle_price_for_A_with_extra():
    # Four A total 180 (130 for three, plus 50 for one extra).
    assert checkout(['A', 'A', 'A', 'A']) == 180

def test_bundle_price_for_B():
    # Two B cost the bundle price of 45 instead of 60.
    assert checkout(['B', 'B']) == 45

def test_bundle_price_for_B_with_extra():
    # Three B total 75 (45 for two, plus 30 for one extra).
    assert checkout(['B', 'B', 'B']) == 75

def test_order_independence():
    # A, B, A, B, A totals 175 in any order.
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175
    assert checkout(['B', 'A', 'A', 'B', 'A']) == 175

def test_every_second_C_free():
    # Two C total 20.
    assert checkout(['C', 'C']) == 20

def test_unpaired_C():
    # Three C total 40 (20 for two, plus 20 for one unpaired).
    assert checkout(['C', 'C', 'C']) == 40

def test_combo_price_for_D_and_C():
    # One D together with one C costs the combo price of 25.
    assert checkout(['D', 'C']) == 25

def test_combo_with_leftovers():
    # D, C and another D total 40 (25 for one D and one C, plus 15 for one extra D).
    assert checkout(['D', 'C', 'D']) == 40

def test_two_D_with_two_C():
    # Two D with two C total 50 (25 for each D-C combo).
    assert checkout(['D', 'C', 'D', 'C']) == 50

def test_produce_pricing():
    # Two kilograms of Apples cost 6.98 (3.49 each).
    assert checkout([('Apples', 2)]) == 6.98

def test_produce_rounding_half_up():
    # Half a kilogram of Bananas costs 1.00 (1.99 per kg).
    assert checkout([('Bananas', 0.5)]) == 1.00

def test_produce_rounding_one_and_half():
    # One and a half kilograms of Bananas cost 2.99 (1.99 per kg).
    assert checkout([('Bananas', 1.5)]) == 2.99

def test_combined_basket_with_weighed_goods():
    # Three A, two B and half a kilogram of Bananas total 176.00.
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00

def test_unknown_item_scan():
    # Scanning an unknown item should return "Unknown item: Grapes".
    with pytest.raises(Exception) as exc_info:
        checkout(['Grapes'])
    assert str(exc_info.value) == "Unknown item: Grapes"

def test_unknown_weight_item_scan():
    # Weighing an unknown item should return "Unknown item: Grapes".
    with pytest.raises(Exception) as exc_info:
        checkout([('Grapes', 1)])
    assert str(exc_info.value) == "Unknown item: Grapes"

def test_zero_weight():
    # Zero weight should raise an error with the message "weight must be positive".
    with pytest.raises(Exception) as exc_info:
        checkout([('Bananas', 0)])
    assert str(exc_info.value) == "weight must be positive"

def test_negative_weight():
    # Negative weight should raise an error with the message "weight must be positive".
    with pytest.raises(Exception) as exc_info:
        checkout([('Bananas', -1)])
    assert str(exc_info.value) == "weight must be positive"