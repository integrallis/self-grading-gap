# test_bookshop.py

import pytest
from solution import calculate_basket_price

# Define valid title identifiers
VALID_TITLES = ['title1', 'title2', 'title3', 'title4', 'title5']

def test_empty_basket():
    # An empty basket costs 0.00
    assert calculate_basket_price([]) == 0.00

def test_single_copy():
    # A single copy costs the base price of 8.00
    for title in VALID_TITLES:
        assert calculate_basket_price([title]) == 8.00

def test_multiple_copies_same_title():
    # Multiple copies of the same title cost the full base price
    assert calculate_basket_price(['title1', 'title1']) == 16.00  # 2 × 8.00
    assert calculate_basket_price(['title2', 'title2', 'title2']) == 24.00  # 3 × 8.00

def test_two_distinct_titles_discount():
    # Two distinct titles cost 15.20 (8.00 + 8.00) * 0.95
    assert calculate_basket_price(['title1', 'title2']) == 15.20

def test_three_distinct_titles_discount():
    # Three distinct titles cost 21.60 (8.00 + 8.00 + 8.00) * 0.90
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60

def test_four_distinct_titles_discount():
    # Four distinct titles cost 25.60 (8.00 + 8.00 + 8.00 + 8.00) * 0.80
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60

def test_five_distinct_titles_discount():
    # All five distinct titles cost 30.00 (8.00 * 5) * 0.75
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00

def test_mixed_basket_with_duplicate():
    # A distinct pair plus a duplicate copy costs 15.20 + 8.00
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 23.20

def test_full_series_plus_one_extra():
    # A full series plus one extra copy costs 30.00 + 8.00
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00

def test_two_of_every_title():
    # Two of every title costs 60.00 (30.00 * 2)
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00

def test_two_four_title_sets():
    # Two copies each of three titles plus one each of the other two costs 51.20
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title5']) == 51.20

def test_doubled_non_greedy_basket():
    # Two copies each of three titles plus one each of the other two costs 102.40 (2 * 51.20)
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title5'] * 2) == 102.40

def test_order_independence():
    # Two copies of each title in different order should yield the same price
    assert calculate_basket_price(['title1', 'title2', 'title1', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == \
           calculate_basket_price(['title5', 'title4', 'title3', 'title2', 'title1', 'title1', 'title2', 'title3', 'title4', 'title5'])

def test_five_complete_series():
    # Five complete series (25 copies) cost 150.00 (5 * 30.00)
    assert calculate_basket_price(['title1', 'title1', 'title1', 'title1', 'title1',
                                    'title2', 'title2', 'title2', 'title2', 'title2',
                                    'title3', 'title3', 'title3', 'title3', 'title3',
                                    'title4', 'title4', 'title4', 'title4', 'title4',
                                    'title5', 'title5', 'title5', 'title5', 'title5']) == 150.00

def test_reject_unknown_titles():
    # A basket containing unknown title raises an error
    with pytest.raises(Exception, match=r"^unknown book: unknown_title$"):
        calculate_basket_price(['title1', 'unknown_title'])

def test_prices_reported_as_numeric_amounts():
    # Prices are reported as numeric amounts in euros
    price = calculate_basket_price(['title1', 'title2', 'title3'])
    assert isinstance(price, (int, float))  # Ensure it's a numeric type