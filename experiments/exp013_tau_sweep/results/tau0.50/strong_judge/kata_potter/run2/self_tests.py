# test_bookshop.py

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

def test_multiple_copies_of_same_title():
    assert calculate_basket_price(['title1', 'title1']) == 16.00  # AC-1.3
    assert calculate_basket_price(['title2', 'title2', 'title2']) == 24.00  # AC-1.3

def test_discount_for_two_distinct_titles():
    assert calculate_basket_price(['title1', 'title2']) == 15.20  # AC-2.1: 8.00 + 8.00 - 5%

def test_discount_for_three_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60  # AC-2.1: 8.00 + 8.00 + 8.00 - 10%

def test_discount_for_four_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60  # AC-2.1: 8.00 + 8.00 + 8.00 + 8.00 - 20%

def test_discount_for_five_distinct_titles():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00  # AC-2.1: 8.00 * 5 - 25%

def test_mixed_basket_with_distinct_and_duplicate_titles():
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 23.20  # AC-3.1: 15.20 (pair) + 8.00 (single)

def test_full_series_plus_one_extra_copy():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00  # AC-3.1: 30.00 (full series) + 8.00 (extra)

def test_two_three_title_sets():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title5']) == 51.20  # AC-3.2: two sets of 4 titles

def test_two_of_every_title():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00  # AC-3.3

def test_doubled_global_optimum_basket():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5'] * 2) == 120.00  # AC-3.3

def test_five_complete_series():
    assert calculate_basket_price(['title1']*5 + ['title2']*5 + ['title3']*5 + ['title4']*5 + ['title5']*5) == 150.00  # AC-3.4

def test_reject_unknown_titles():
    with pytest.raises(Exception) as excinfo:
        calculate_basket_price(['title1', 'unknown_title'])
    assert str(excinfo.value) == "unknown book: unknown_title"  # AC-4.1

    with pytest.raises(Exception) as excinfo:
        calculate_basket_price(['unknown_title'])
    assert str(excinfo.value) == "unknown book: unknown_title"  # AC-4.1

def test_prices_reported_as_numeric_amounts():
    assert isinstance(calculate_basket_price(['title1']), (int, float))  # AC-4.2
    assert isinstance(calculate_basket_price(['title1', 'title2']), (int, float))  # AC-4.2

def test_permutation_invariance():
    basket1 = ['title1', 'title2', 'title3', 'title1']
    basket2 = ['title1', 'title3', 'title2', 'title1']
    assert calculate_basket_price(basket1) == calculate_basket_price(basket2)  # AC-3.3