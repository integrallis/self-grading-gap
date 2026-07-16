# test_bookshop.py
from solution import calculate_basket_price

def test_empty_basket_costs_zero():
    # An empty basket costs 0.00
    assert calculate_basket_price([]) == 0.00

def test_single_copy_costs_base_price():
    # A single copy costs the base price of 8.00
    assert calculate_basket_price(['title1']) == 8.00
    assert calculate_basket_price(['title2']) == 8.00
    assert calculate_basket_price(['title3']) == 8.00
    assert calculate_basket_price(['title4']) == 8.00
    assert calculate_basket_price(['title5']) == 8.00

def test_multiple_copies_of_same_title_cost_full_price():
    # Multiple copies of the same title cost the base price each
    assert calculate_basket_price(['title1', 'title1']) == 16.00
    assert calculate_basket_price(['title2', 'title2', 'title2']) == 24.00

def test_discount_for_two_distinct_titles():
    # Two distinct titles cost 15.20 (8.00 + 8.00 - 5%)
    assert calculate_basket_price(['title1', 'title2']) == 15.20

def test_discount_for_three_distinct_titles():
    # Three distinct titles cost 21.60 (24.00 - 10%)
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60

def test_discount_for_four_distinct_titles():
    # Four distinct titles cost 25.60 (32.00 - 20%)
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60

def test_discount_for_five_distinct_titles():
    # Five distinct titles cost 30.00 (40.00 - 25%)
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00

def test_mixed_basket_with_duplicate_and_distinct_titles():
    # A distinct pair plus a duplicate copy costs 15.20 + 8.00 = 23.20
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 23.20

def test_full_series_plus_one_extra_copy():
    # A full series plus one extra copy costs 38.00
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00

def test_two_sets_of_four_titles():
    # Two copies each of three titles plus one each of the other two costs 51.20
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title5']) == 51.20

def test_large_basket_correctly_priced():
    # Five complete series (25 copies) cost 150.00
    assert calculate_basket_price(['title1'] * 5 + ['title2'] * 5 + ['title3'] * 5 + ['title4'] * 5 + ['title5'] * 5) == 150.00

def test_unknown_title_rejected():
    # A basket with an unknown title should raise an error
    with pytest.raises(ValueError, match="unknown book: unknown_title"):
        calculate_basket_price(['title1', 'unknown_title'])

def test_prices_reported_as_numeric_amounts():
    # The price should be reported as numeric amounts in euros
    assert isinstance(calculate_basket_price(['title1']), float)
    assert isinstance(calculate_basket_price(['title1', 'title2']), float)