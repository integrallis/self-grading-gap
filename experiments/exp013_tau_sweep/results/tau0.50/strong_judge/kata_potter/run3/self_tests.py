# test_bookshop.py

from solution import calculate_basket_price

def test_empty_basket_costs_zero():
    assert calculate_basket_price([]) == 0.00  # AC-1.1

def test_single_copy_costs_base_price():
    assert calculate_basket_price(['title_1']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title_2']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title_3']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title_4']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title_5']) == 8.00  # AC-1.2

def test_multiple_copies_of_same_title_costs_full_price():
    assert calculate_basket_price(['title_1', 'title_1']) == 16.00  # AC-1.3
    assert calculate_basket_price(['title_2', 'title_2', 'title_2']) == 24.00  # AC-1.3

def test_discount_for_two_distinct_titles():
    assert calculate_basket_price(['title_1', 'title_2']) == 15.20  # AC-2.1: 8 + 8 - 5%

def test_discount_for_three_distinct_titles():
    assert calculate_basket_price(['title_1', 'title_2', 'title_3']) == 21.60  # AC-2.1: 8 + 8 + 8 - 10%

def test_discount_for_four_distinct_titles():
    assert calculate_basket_price(['title_1', 'title_2', 'title_3', 'title_4']) == 25.60  # AC-2.1: 8 + 8 + 8 + 8 - 20%

def test_discount_for_five_distinct_titles():
    assert calculate_basket_price(['title_1', 'title_2', 'title_3', 'title_4', 'title_5']) == 30.00  # AC-2.1: 8 * 5 - 25%

def test_mixed_basket_with_repeated_titles():
    assert calculate_basket_price(['title_1', 'title_2', 'title_1']) == 23.20  # AC-3.1: (15.20 + 8.00)

def test_full_series_plus_one_extra_copy():
    assert calculate_basket_price(['title_1', 'title_2', 'title_3', 'title_4', 'title_5', 'title_1']) == 38.00  # AC-3.1: (30.00 + 8.00)

def test_two_four_title_sets_beat_five_plus_three():
    assert calculate_basket_price(['title_1', 'title_1', 'title_2', 'title_2', 'title_3', 'title_3', 'title_4', 'title_5']) == 51.20  # AC-3.2

def test_two_of_every_title():
    assert calculate_basket_price(['title_1', 'title_1', 'title_2', 'title_2', 'title_3', 'title_3', 'title_4', 'title_4', 'title_5', 'title_5']) == 60.00  # AC-3.3

def test_five_complete_series():
    assert calculate_basket_price(['title_1'] * 5 + ['title_2'] * 5 + ['title_3'] * 5 + ['title_4'] * 5 + ['title_5'] * 5) == 150.00  # AC-3.4

def test_unknown_title_is_rejected():
    try:
        calculate_basket_price(['unknown_title'])
    except ValueError as e:
        assert str(e) == "unknown book: unknown_title"  # AC-4.1

def test_mixed_basket_with_unknown_title_is_rejected():
    try:
        calculate_basket_price(['title_1', 'unknown_title'])
    except ValueError as e:
        assert str(e) == "unknown book: unknown_title"  # AC-4.1

def test_prices_are_reported_as_numeric_amounts():
    price = calculate_basket_price(['title_1'])
    assert isinstance(price, (float, int))  # AC-4.2
    price = calculate_basket_price(['title_1', 'title_2'])
    assert isinstance(price, (float, int))  # AC-4.2

def test_basket_price_is_order_independent():
    basket1 = ['title_1', 'title_2', 'title_3']
    basket2 = ['title_3', 'title_2', 'title_1']
    assert calculate_basket_price(basket1) == calculate_basket_price(basket2)  # AC-3.3

def test_doubled_ac3_2_basket():
    assert calculate_basket_price(['title_1', 'title_1', 'title_2', 'title_2', 'title_3', 'title_3', 'title_4', 'title_4', 'title_5', 'title_5']) == 102.40  # AC-3.2

def test_performance_large_basket():
    assert calculate_basket_price(['title_1'] * 50 + ['title_2'] * 50 + ['title_3'] * 50 + ['title_4'] * 50 + ['title_5'] * 50) == 1500.00  # AC-3.4