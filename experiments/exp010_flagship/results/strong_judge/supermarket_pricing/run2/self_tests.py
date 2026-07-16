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

def test_three_A_bundle_price():
    assert checkout(['A', 'A', 'A']) == 130  # AC-2.1

def test_four_A_bundle_price():
    assert checkout(['A', 'A', 'A', 'A']) == 180  # AC-2.2

def test_two_B_bundle_price():
    assert checkout(['B', 'B']) == 45  # AC-2.3

def test_three_B_bundle_price():
    assert checkout(['B', 'B', 'B']) == 75  # AC-2.4

def test_order_independence_of_A_and_B():
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # AC-2.5
    assert checkout(['B', 'A', 'B', 'A', 'A']) == 175  # AC-2.5
    assert checkout(['A', 'A', 'B', 'A', 'B']) == 175  # AC-2.5
    assert checkout(['B', 'A', 'A', 'B', 'A']) == 175  # AC-2.5

def test_two_C_total_price():
    assert checkout(['C', 'C']) == 20  # AC-3.1

def test_three_C_total_price():
    assert checkout(['C', 'C', 'C']) == 40  # AC-3.2

def test_one_D_and_one_C_combo_price():
    assert checkout(['D', 'C']) == 25  # AC-4.1

def test_combination_with_leftover_D():
    assert checkout(['D', 'C', 'D']) == 40  # AC-4.2

def test_combination_with_two_D_and_two_C():
    assert checkout(['D', 'C', 'D', 'C']) == 50  # AC-4.2

def test_banana_weight_price():
    assert checkout([('Bananas', 1)]) == 1.99  # AC-5.1

def test_apples_weight_price():
    assert checkout([('Apples', 2)]) == 6.98  # AC-5.1

def test_banana_half_kilogram_price():
    assert checkout([('Bananas', 0.5)]) == 1.00  # AC-5.2

def test_banana_one_and_half_kilograms_price():
    assert checkout([('Bananas', 1.5)]) == 2.99  # AC-5.2

def test_multiple_banana_half_kilogram_lines():
    assert checkout([('Bananas', 0.5), ('Bananas', 0.5)]) == 2.00  # AC-5.2

def test_combined_basket_with_weighed_goods():
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00  # AC-5.3
    assert checkout(['D', 'C', ('Bananas', 0.5)]) == 26.00  # AC-5.3

def test_unknown_item_scan():
    result = checkout(['X'])  # AC-6.1
    assert result == "Unknown item: X"

def test_unknown_weighted_item_scan():
    result = checkout([('Grapes', 1)])  # AC-6.2
    assert result == "Unknown item: Grapes"

def test_zero_weight_item():
    result = checkout([('Bananas', 0)])  # AC-6.3
    assert result == "weight must be positive"

def test_negative_weight_item():
    result = checkout([('Bananas', -1)])  # AC-6.3
    assert result == "weight must be positive"