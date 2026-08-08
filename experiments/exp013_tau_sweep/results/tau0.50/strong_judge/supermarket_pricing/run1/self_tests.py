# test_supermarket_checkout.py

import pytest
from solution import checkout

def test_empty_basket_totals_zero():
    assert checkout([]) == 0  # AC-1.1

def test_unit_prices():
    assert checkout(['A']) == 50  # AC-1.2
    assert checkout(['B']) == 30  # AC-1.2
    assert checkout(['C']) == 20  # AC-1.2
    assert checkout(['D']) == 15  # AC-1.2

def test_different_items_add_prices():
    assert checkout(['A', 'B']) == 80  # AC-1.3

def test_multiple_units_no_promotion():
    assert checkout(['D', 'D']) == 30  # AC-1.4

def test_bundle_price_three_A():
    assert checkout(['A', 'A', 'A']) == 130  # AC-2.1

def test_bundle_price_four_A():
    assert checkout(['A', 'A', 'A', 'A']) == 180  # AC-2.2

def test_bundle_price_two_B():
    assert checkout(['B', 'B']) == 45  # AC-2.3

def test_bundle_price_three_B():
    assert checkout(['B', 'B', 'B']) == 75  # AC-2.4

def test_total_order_independence():
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # AC-2.5
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175  # AC-2.5
    assert checkout(['A', 'A', 'B', 'B', 'A']) == 175  # AC-2.5
    assert checkout(['B', 'A', 'A', 'B', 'A']) == 175  # AC-2.5

def test_every_second_C_free():
    assert checkout(['C', 'C']) == 20  # AC-3.1

def test_unpaired_C():
    assert checkout(['C', 'C', 'C']) == 40  # AC-3.2

def test_combo_price_one_D_and_one_C():
    assert checkout(['D', 'C']) == 25  # AC-4.1

def test_combo_price_with_leftovers():
    assert checkout(['D', 'C', 'D']) == 40  # AC-4.2
    assert checkout(['D', 'C', 'D', 'C']) == 50  # AC-4.2

def test_weighted_goods_price_per_kg():
    assert checkout(['Bananas', 1]) == 1.99  # AC-5.1
    assert checkout(['Apples', 2]) == 6.98  # AC-5.1

def test_weighted_goods_rounding():
    assert checkout(['Bananas', 0.5]) == 1.00  # AC-5.2
    assert checkout(['Bananas', 1.5]) == 2.99  # AC-5.2
    assert checkout(['Bananas', 0.6]) == 1.19  # AC-5.2 rounding non-half
    assert checkout(['Apples', 0.5]) == 1.75  # AC-5.2 rounding half-up

def test_combined_basket_with_weighted_goods():
    assert checkout(['A', 'A', 'A', 'B', 'B', 'Bananas', 0.5]) == 176.00  # AC-5.3

def test_unknown_item_scan():
    with pytest.raises(ValueError) as excinfo:
        checkout(['UnknownItem'])
    assert str(excinfo.value) == "Unknown item: UnknownItem"  # AC-6.1

def test_unknown_weigh_item_scan():
    with pytest.raises(ValueError) as excinfo:
        checkout(['Grapes', 1])
    assert str(excinfo.value) == "Unknown item: Grapes"  # AC-6.2

def test_weigh_item_weight_positive():
    with pytest.raises(ValueError) as excinfo:
        checkout(['Bananas', 0])
    assert str(excinfo.value) == "weight must be positive"  # AC-6.3

def test_weigh_item_weight_negative():
    with pytest.raises(ValueError) as excinfo:
        checkout(['Bananas', -1])
    assert str(excinfo.value) == "weight must be positive"  # AC-6.3

def test_bundle_price_six_A():
    assert checkout(['A', 'A', 'A', 'A', 'A', 'A']) == 260  # six A total

def test_bundle_price_four_B():
    assert checkout(['B', 'B', 'B', 'B']) == 90  # four B total

def test_unpaired_C_with_combo():
    assert checkout(['D', 'C', 'C']) == 40  # D and one C combo, the other C is unpaired