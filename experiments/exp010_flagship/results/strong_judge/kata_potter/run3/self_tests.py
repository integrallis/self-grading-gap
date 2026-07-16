import pytest
from solution import *  # Importing all public names from the solution package

def test_empty_basket():
    # An empty basket costs 0.00 euros.
    assert calculate_price([]) == 0.00

def test_single_copy():
    # A single copy costs the base price of 8.00 euros.
    assert calculate_price(['title1']) == 8.00
    assert calculate_price(['title2']) == 8.00
    assert calculate_price(['title3']) == 8.00
    assert calculate_price(['title4']) == 8.00
    assert calculate_price(['title5']) == 8.00

def test_multiple_copies_of_same_title():
    # Multiple copies of the same title cost the full base price.
    assert calculate_price(['title1', 'title1']) == 16.00
    assert calculate_price(['title2', 'title2', 'title2']) == 24.00

def test_discounted_sets_of_distinct_titles():
    # A set of 2 distinct titles costs 15.20 euros (8 * 2 - 5%).
    assert calculate_price(['title1', 'title2']) == 15.20
    # A set of 3 distinct titles costs 21.60 euros (8 * 3 - 10%).
    assert calculate_price(['title1', 'title2', 'title3']) == 21.60
    # A set of 4 distinct titles costs 25.60 euros (8 * 4 - 20%).
    assert calculate_price(['title1', 'title2', 'title3', 'title4']) == 25.60
    # A full series of 5 distinct titles costs 30.00 euros (8 * 5 - 25%).
    assert calculate_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00

def test_mixed_basket_with_repeated_titles():
    # A distinct pair plus a duplicate copy costs 15.20 + 8.00 = 23.20 euros.
    assert calculate_price(['title1', 'title2', 'title1']) == 23.20
    # A full series plus one extra copy costs 30.00 + 8.00 = 38.00 euros.
    assert calculate_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00
    # Two of every title costs 60.00 euros.
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00

def test_grouping_is_globally_optimal():
    # Two copies each of three titles plus one each of the other two costs 51.20 euros.
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title5']) == 51.20
    # Doubling that basket costs 102.40 euros.
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 
                            'title4', 'title5', 'title1', 'title1', 'title2', 'title2', 
                            'title3', 'title3', 'title4', 'title5']) == 102.40

def test_large_baskets():
    # Five complete series (25 copies) cost 150.00 euros.
    assert calculate_price(['title1'] * 5 + ['title2'] * 5 + ['title3'] * 5 + ['title4'] * 5 + ['title5'] * 5) == 150.00

def test_reject_unknown_titles():
    # A basket containing an unknown title should raise an error.
    with pytest.raises(Exception) as excinfo:
        calculate_price(['title1', 'unknown_title'])
    assert str(excinfo.value) == "unknown book: unknown_title"

    with pytest.raises(Exception) as excinfo:
        calculate_price(['unknown_title'])
    assert str(excinfo.value) == "unknown book: unknown_title"

def test_order_independence():
    # The same multiset in different orders should yield the same price.
    basket1 = ['title1', 'title2', 'title3', 'title4']
    basket2 = ['title4', 'title3', 'title2', 'title1']
    assert calculate_price(basket1) == calculate_price(basket2)

    # Testing a mixed basket with duplicates in different order.
    basket3 = ['title1', 'title1', 'title2', 'title3', 'title4']
    basket4 = ['title4', 'title3', 'title2', 'title1', 'title1']
    assert calculate_price(basket3) == calculate_price(basket4)