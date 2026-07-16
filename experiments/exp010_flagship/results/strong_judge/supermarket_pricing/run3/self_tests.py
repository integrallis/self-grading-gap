from solution import checkout
import pytest

def test_empty_basket_totals_zero():
    assert checkout([]) == 0  # AC-1.1: An empty basket totals 0.

def test_unit_prices():
    assert checkout(["A"]) == 50  # AC-1.2: A costs 50.
    assert checkout(["B"]) == 30  # AC-1.2: B costs 30.
    assert checkout(["C"]) == 20  # AC-1.2: C costs 20.
    assert checkout(["D"]) == 15  # AC-1.2: D costs 15.

def test_different_items_total():
    assert checkout(["A", "B"]) == 80  # AC-1.3: A with B totals 80.
    
def test_multiple_units_no_promotion():
    assert checkout(["D", "D"]) == 30  # AC-1.4: Two D total 30.

def test_bundle_deal_three_A():
    assert checkout(["A", "A", "A"]) == 130  # AC-2.1: Three A cost 130 instead of 150.

def test_bundle_deal_four_A():
    assert checkout(["A", "A", "A", "A"]) == 180  # AC-2.2: Four A total 180.

def test_bundle_deal_two_B():
    assert checkout(["B", "B"]) == 45  # AC-2.3: Two B cost 45 instead of 60.

def test_bundle_deal_three_B():
    assert checkout(["B", "B", "B"]) == 75  # AC-2.4: Three B total 75.

def test_bundle_deal_order_independence():
    assert checkout(["A", "B", "A", "B", "A"]) == 175  # AC-2.5: A, B, A, B, A totals 175 in any order.
    assert checkout(["B", "A", "B", "A", "A"]) == 175  # AC-2.5: A, B, A, B, A totals 175 in any order.

def test_buy_one_get_one_free_C_two():
    assert checkout(["C", "C"]) == 20  # AC-3.1: Two C total 20.

def test_buy_one_get_one_free_C_three():
    assert checkout(["C", "C", "C"]) == 40  # AC-3.2: Three C total 40.

def test_combo_price_D_and_C():
    assert checkout(["D", "C"]) == 25  # AC-4.1: One D and one C costs 25.

def test_combo_price_leftovers():
    assert checkout(["D", "C", "D"]) == 40  # AC-4.2: D, C and another D total 40.

def test_combo_price_two_pairs():
    assert checkout(["D", "C", "D", "C"]) == 50  # AC-4.2: Two D with two C total 50.

def test_weighed_goods_price():
    assert checkout([("Bananas", 2)]) == 3.98  # AC-5.1: Two kilograms of Bananas cost 3.98.
    assert checkout([("Apples", 2)]) == 6.98  # AC-5.1: Two kilograms of Apples cost 6.98.

def test_weighed_goods_rounding():
    assert checkout([("Bananas", 0.5)]) == 1.00  # AC-5.2: Half a kilogram of Bananas is 1.00.
    assert checkout([("Bananas", 1.5)]) == 2.99  # AC-5.2: One and a half kilograms is 2.99.
    assert checkout([("Bananas", 0.5), ("Bananas", 0.5)]) == 2.00  # AC-5.2: Two half kg of Bananas total 2.00.

def test_mixed_basket():
    assert checkout(["A", "A", "A", "B", "B", ("Bananas", 0.5)]) == 176.00  # AC-5.3: Total is 176.00.

def test_unknown_item_scan():
    with pytest.raises(Exception) as exc_info:
        checkout(["X"])
    assert str(exc_info.value) == "Unknown item: X"  # AC-6.1: Unknown item scan refused.

def test_unknown_weight_item_scan():
    with pytest.raises(Exception) as exc_info:
        checkout([("Grapes", 1)])
    assert str(exc_info.value) == "Unknown item: Grapes"  # AC-6.2: Unknown weight item scan refused.

def test_negative_weight():
    with pytest.raises(Exception) as exc_info:
        checkout([("Bananas", -1)])
    assert str(exc_info.value) == "weight must be positive"  # AC-6.3: Negative weight refused.

def test_zero_weight():
    with pytest.raises(Exception) as exc_info:
        checkout([("Apples", 0)])
    assert str(exc_info.value) == "weight must be positive"  # AC-6.3: Zero weight refused.

def test_bundle_deal_six_A():
    assert checkout(["A", "A", "A", "A", "A", "A"]) == 260  # AC-2.1: Six A total 260.

def test_bundle_deal_four_B():
    assert checkout(["B", "B", "B", "B"]) == 90  # AC-2.3: Four B total 90.

def test_buy_one_get_one_free_C_four():
    assert checkout(["C", "C", "C", "C"]) == 40  # AC-3.1: Four C total 40.

def test_bundle_deal_order_independence_for_combo():
    assert checkout(["D", "C", "D", "C"]) == 50  # AC-4.2: Two D with two C total 50.
    assert checkout(["C", "D", "C", "D"]) == 50  # AC-4.2: Two D with two C total 50.