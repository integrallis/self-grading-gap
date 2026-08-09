# test_bookshop.py

import pytest
from solution import calculate_price

VALID_TITLES = ['book1', 'book2', 'book3', 'book4', 'book5']

def test_empty_basket_costs_zero():
    assert calculate_price([]) == 0.00  # AC-1.1: An empty basket costs 0.00.

def test_single_copy_costs_base_price():
    assert calculate_price(['book1']) == 8.00  # AC-1.2: A single copy costs 8.00.

def test_multiple_copies_of_same_title_costs_full_price():
    assert calculate_price(['book1', 'book1']) == 16.00  # AC-1.3: Two copies of the same title cost 16.00.

def test_two_distinct_titles_discount():
    assert calculate_price(['book1', 'book2']) == 15.20  # AC-2.1: Two distinct titles cost 15.20.

def test_three_distinct_titles_discount():
    assert calculate_price(['book1', 'book2', 'book3']) == 21.60  # AC-2.1: Three distinct titles cost 21.60.

def test_four_distinct_titles_discount():
    assert calculate_price(['book1', 'book2', 'book3', 'book4']) == 25.60  # AC-2.1: Four distinct titles cost 25.60.

def test_five_distinct_titles_discount():
    assert calculate_price(['book1', 'book2', 'book3', 'book4', 'book5']) == 30.00  # AC-2.1: Five distinct titles cost 30.00.

def test_mixed_basket_with_duplicate_title():
    assert calculate_price(['book1', 'book1', 'book2']) == 23.20  # AC-3.1: Pair plus a duplicate costs 23.20.

def test_full_series_plus_one_extra_cost():
    assert calculate_price(['book1', 'book2', 'book3', 'book4', 'book5', 'book5']) == 38.00  # AC-3.1: Full series plus one extra costs 38.00.

def test_two_of_every_title_cost():
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book4', 'book5', 'book5']) == 60.00  # AC-3.1: Two of every title costs 60.00.

def test_two_four_title_sets_cost():
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book4']) == 51.20  # AC-3.2: Two four-title sets cost 51.20.

def test_non_greedy_basket_cost():
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book5']) == 51.20  # AC-3.2: Non-greedy grouping costs 51.20.

def test_doubled_non_greedy_basket_cost():
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book5'] * 2) == 102.40  # AC-3.2: Doubled basket costs 102.40.

def test_large_basket_correct_price():
    assert calculate_price(['book1'] * 5 + ['book2'] * 5 + ['book3'] * 5 + ['book4'] * 5 + ['book5'] * 5) == 150.00  # AC-3.4: Five complete series cost 150.00.

def test_unknown_title_rejected():
    with pytest.raises(Exception) as excinfo:
        calculate_price(['book1', 'unknown_title'])
    assert str(excinfo.value) == "unknown book: unknown_title"  # AC-4.1: Reject unknown title.

def test_prices_reported_as_numeric_amounts():
    price = calculate_price(['book1', 'book2'])
    assert price >= 0  # AC-4.2: Prices are reported as numeric amounts.

def test_order_independence():
    assert calculate_price(['book1', 'book2', 'book3']) == calculate_price(['book3', 'book2', 'book1'])  # AC-3.3: Order independence.

def test_order_independence_with_duplicates():
    assert calculate_price(['book1', 'book1', 'book2']) == calculate_price(['book2', 'book1', 'book1'])  # AC-3.3: Order independence with duplicates.