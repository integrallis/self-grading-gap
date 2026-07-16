from solution import checkout

def test_empty_basket_totals_zero():
    assert checkout([]) == 0  # AC-1.1

def test_unit_prices():
    assert checkout(['A']) == 50  # AC-1.2
    assert checkout(['B']) == 30  # AC-1.2
    assert checkout(['C']) == 20  # AC-1.2
    assert checkout(['D']) == 15  # AC-1.2

def test_different_items_add_prices():
    assert checkout(['A', 'B']) == 80  # AC-1.3 (50 + 30)

def test_multiple_units_no_promotion():
    assert checkout(['D', 'D']) == 30  # AC-1.4 (15 + 15)

def test_bundle_price_for_three_A():
    assert checkout(['A', 'A', 'A']) == 130  # AC-2.1 (130 instead of 150)

def test_bundle_price_for_four_A():
    assert checkout(['A', 'A', 'A', 'A']) == 180  # AC-2.2 (130 + 50)

def test_bundle_price_for_two_B():
    assert checkout(['B', 'B']) == 45  # AC-2.3 (45 instead of 60)

def test_bundle_price_for_three_B():
    assert checkout(['B', 'B', 'B']) == 75  # AC-2.4 (45 + 30)

def test_total_independence_of_order_A_B():
    assert checkout(['A', 'B', 'A', 'B', 'A']) == 175  # AC-2.5

def test_every_second_C_free():
    assert checkout(['C', 'C']) == 20  # AC-3.1 (20 for two C)

def test_unpaired_C_is_unit_price():
    assert checkout(['C', 'C', 'C']) == 40  # AC-3.2 (20 + 20)

def test_combo_price_for_D_and_C():
    assert checkout(['D', 'C']) == 25  # AC-4.1

def test_combo_with_leftover_D_and_C():
    assert checkout(['D', 'C', 'D']) == 40  # AC-4.2 (25 + 15)

def test_combo_with_two_D_and_two_C():
    assert checkout(['D', 'C', 'D', 'C']) == 50  # AC-4.2 (25 + 25)

def test_price_for_banana_weighed_goods():
    assert checkout([('Bananas', 1)]) == 1.99  # AC-5.1

def test_price_for_apples_weighed_goods():
    assert checkout([('Apples', 2)]) == 6.98  # AC-5.1 (2 * 3.49)

def test_rounding_half_a_kg_banana():
    assert checkout([('Bananas', 0.5)]) == 1.00  # AC-5.2 (0.995 rounds to 1.00)

def test_rounding_one_and_half_a_kg_banana():
    assert checkout([('Bananas', 1.5)]) == 2.99  # AC-5.2 (2.985 rounds to 2.99)

def test_combined_total_with_weighed_goods():
    assert checkout(['A', 'A', 'A', 'B', 'B', ('Bananas', 0.5)]) == 176.00  # AC-5.3

def test_unknown_item_scan():
    try:
        checkout(['X'])
    except ValueError as e:
        assert str(e) == "Unknown item: X"  # AC-6.1

def test_unknown_weighed_item_scan():
    try:
        checkout([('Grapes', 1)])
    except ValueError as e:
        assert str(e) == "Unknown item: Grapes"  # AC-6.2

def test_zero_weight_item_refused():
    try:
        checkout([('Bananas', 0)])
    except ValueError as e:
        assert str(e) == "weight must be positive"  # AC-6.3

def test_negative_weight_item_refused():
    try:
        checkout([('Bananas', -1)])
    except ValueError as e:
        assert str(e) == "weight must be positive"  # AC-6.3