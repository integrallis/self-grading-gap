import pytest
from solution import calculate_basket_price

def test_empty_basket_costs_zero():
    assert calculate_basket_price([]) == 0.00  # AC-1.1

def test_single_copy_costs_base_price():
    assert calculate_basket_price(['title1']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title2']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title3']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title4']) == 8.00  # AC-1.2
    assert calculate_basket_price(['title5']) == 8.00  # AC-1.2

def test_multiple_copies_of_same_title_costs_full_price():
    assert calculate_basket_price(['title1', 'title1']) == 16.00  # AC-1.3
    assert calculate_basket_price(['title2', 'title2', 'title2']) == 24.00  # AC-1.3

def test_discounted_price_for_two_distinct_titles():
    assert calculate_basket_price(['title1', 'title2']) == 15.20  # AC-2.1 (8.00 + 8.00) * 0.95

def test_discounted_price_for_three_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60  # AC-2.1 (8.00 + 8.00 + 8.00) * 0.90

def test_discounted_price_for_four_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60  # AC-2.1 (8.00 * 4) * 0.80

def test_discounted_price_for_five_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00  # AC-2.1 (8.00 * 5) * 0.75

def test_price_for_mixed_basket_optimally():
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 23.20  # AC-3.1 (15.20 + 8.00)

def test_price_for_full_series_plus_one_extra():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00  # AC-3.1 (30.00 + 8.00)

def test_price_for_two_of_every_title():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00  # AC-3.1 (30.00 * 2)

def test_price_for_non_greedy_basket():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5']) == 51.20  # AC-3.2 (25.60 * 2)

def test_price_for_doubled_non_greedy_basket():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5'] * 2) == 111.20  # AC-3.2 (51.20 * 2)

def test_order_does_not_affect_price():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == calculate_basket_price(['title1', 'title5', 'title4', 'title3', 'title2', 'title1'])  # AC-3.3

def test_large_basket_pricing():
    assert calculate_basket_price(['title1'] * 5 + ['title2'] * 5 + ['title3'] * 5 + ['title4'] * 5 + ['title5'] * 5) == 150.00  # AC-3.4 (30.00 * 5)

def test_reject_unknown_titles():
    with pytest.raises(Exception) as exc_info:
        calculate_basket_price(['title1', 'unknown_title'])
    assert str(exc_info.value) == "unknown book: unknown_title"  # AC-4.1

    with pytest.raises(Exception) as exc_info:
        calculate_basket_price(['unknown_title'])
    assert str(exc_info.value) == "unknown book: unknown_title"  # AC-4.1

def test_price_reported_as_numeric_amount():
    assert isinstance(calculate_basket_price(['title1']), (int, float))  # AC-4.2

def test_performance_for_large_basket():
    import time
    start_time = time.time()
    calculate_basket_price(['title1'] * 25)
    assert time.time() - start_time < 1.0  # AC-3.4 reasonable time check