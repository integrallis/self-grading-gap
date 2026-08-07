# test_bookshop.py

import pytest
from solution import calculate_price

def test_empty_basket_costs_zero():
    # An empty basket costs 0.00 euros.
    assert calculate_price([]) == 0.00

def test_single_copy_costs_base_price():
    # A single copy costs the base price of 8.00 euros.
    assert calculate_price(['book1']) == 8.00
    assert calculate_price(['book2']) == 8.00
    assert calculate_price(['book3']) == 8.00
    assert calculate_price(['book4']) == 8.00
    assert calculate_price(['book5']) == 8.00

def test_multiple_copies_of_same_title_cost_full_price():
    # Multiple copies of the same title never form a discounted set.
    assert calculate_price(['book1', 'book1']) == 16.00
    assert calculate_price(['book2', 'book2', 'book2']) == 24.00

def test_discounted_price_for_two_distinct_titles():
    # A set of two distinct titles costs 15.20 euros (5% discount).
    assert calculate_price(['book1', 'book2']) == 15.20

def test_discounted_price_for_three_distinct_titles():
    # A set of three distinct titles costs 21.60 euros (10% discount).
    assert calculate_price(['book1', 'book2', 'book3']) == 21.60

def test_discounted_price_for_four_distinct_titles():
    # A set of four distinct titles costs 25.60 euros (20% discount).
    assert calculate_price(['book1', 'book2', 'book3', 'book4']) == 25.60

def test_discounted_price_for_five_distinct_titles():
    # A full series of five distinct titles costs 30.00 euros (25% discount).
    assert calculate_price(['book1', 'book2', 'book3', 'book4', 'book5']) == 30.00

def test_price_for_mixed_basket_with_duplicates():
    # A distinct pair plus a duplicate copy costs 15.20 + 8.00 = 23.20 euros.
    assert calculate_price(['book1', 'book2', 'book1']) == 23.20

def test_price_for_full_series_plus_one_extra():
    # A full series plus one extra copy costs 30.00 + 8.00 = 38.00 euros.
    assert calculate_price(['book1', 'book2', 'book3', 'book4', 'book5', 'book1']) == 38.00

def test_price_for_two_of_every_title():
    # Two of every title costs 2 * 30.00 = 60.00 euros.
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book4', 'book5', 'book5']) == 60.00

def test_grouping_is_globally_optimal():
    # Two copies each of three titles plus one each of the other two costs 51.20 euros.
    assert calculate_price(['book1', 'book1', 'book2', 'book2', 'book3', 'book3', 'book4', 'book5']) == 51.20

def test_price_for_large_baskets():
    # Five complete series (25 copies) cost 5 * 30.00 = 150.00 euros.
    assert calculate_price(['book1'] * 5 + ['book2'] * 5 + ['book3'] * 5 + ['book4'] * 5 + ['book5'] * 5) == 150.00

def test_reject_unknown_titles():
    # A basket containing an unknown title raises an error.
    with pytest.raises(Exception) as excinfo:
        calculate_price(['book1', 'unknown_book'])
    assert str(excinfo.value) == "unknown book: unknown_book"

def test_price_reported_as_numeric_amount():
    # Prices must be returned as numeric amounts in euros.
    price = calculate_price(['book1'])
    assert isinstance(price, (int, float))  # Check if the price is a numeric amount

def test_doubled_optimal_grouping():
    # Four copies each of three titles (4*3 = 12) and two copies each of the remaining two titles (2*2 = 4) costs 102.40 euros.
    assert calculate_price(['book1', 'book1', 'book1', 'book1', 'book2', 'book2', 'book2', 'book2', 'book3', 'book3', 'book3', 'book3', 'book4', 'book4']) == 102.40

def test_order_independence():
    # Check that the price is the same for the same title count in different orders.
    assert calculate_price(['book1', 'book1', 'book2', 'book2']) == calculate_price(['book2', 'book2', 'book1', 'book1'])