# your complete test file
import pytest
from solution import calculate_price

def test_empty_basket_costs_zero():
    assert calculate_price([]) == 0.00  # AC-1.1: An empty basket costs 0.00

def test_single_copy_costs_base_price():
    assert calculate_price(['title1']) == 8.00  # AC-1.2: A single copy costs the base price of 8.00
    assert calculate_price(['title2']) == 8.00  # AC-1.2: A single copy costs the base price of 8.00
    assert calculate_price(['title3']) == 8.00  # AC-1.2: A single copy costs the base price of 8.00
    assert calculate_price(['title4']) == 8.00  # AC-1.2: A single copy costs the base price of 8.00
    assert calculate_price(['title5']) == 8.00  # AC-1.2: A single copy costs the base price of 8.00

def test_multiple_copies_of_same_title_costs_full_price():
    assert calculate_price(['title1', 'title1']) == 16.00  # AC-1.3: Two copies of the same title cost 16.00

def test_two_distinct_titles_discounted():
    assert calculate_price(['title1', 'title2']) == 15.20  # AC-2.1: Two distinct titles cost 15.20

def test_three_distinct_titles_discounted():
    assert calculate_price(['title1', 'title2', 'title3']) == 21.60  # AC-2.1: Three distinct titles cost 21.60

def test_four_distinct_titles_discounted():
    assert calculate_price(['title1', 'title2', 'title3', 'title4']) == 25.60  # AC-2.1: Four distinct titles cost 25.60

def test_five_distinct_titles_discounted():
    assert calculate_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00  # AC-2.1: Five distinct titles cost 30.00

def test_pair_plus_duplicate_costs():
    assert calculate_price(['title1', 'title2', 'title1']) == 23.20  # AC-3.1: (15.20 + 8.00)

def test_full_series_plus_extra_copy_costs():
    assert calculate_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00  # AC-3.1: (30.00 + 8.00)

def test_two_copies_of_each_title_costs():
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00  # AC-3.1: (30.00 + 30.00)

def test_two_four_title_sets_cheaper_than_full_series():
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5']) == 51.20  # AC-3.2: (25.60 + 25.60)

def test_two_four_title_sets_cheaper_than_full_series_doubled():
    assert calculate_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4']) == 102.40  # AC-3.2: (51.20 * 2)

def test_large_basket_correct_pricing():
    assert calculate_price(['title1', 'title1', 'title1', 'title1', 'title1', 
                            'title2', 'title2', 'title2', 'title2', 'title2', 
                            'title3', 'title3', 'title3', 'title3', 'title3', 
                            'title4', 'title4', 'title4', 'title4', 'title4', 
                            'title5', 'title5', 'title5', 'title5', 'title5']) == 150.00  # AC-3.4: 5 complete series cost 150.00

def test_unknown_title_rejected():
    with pytest.raises(Exception, match=r"^unknown book: title6$"):
        calculate_price(['title6'])  # AC-4.1: Unknown title should raise an error

def test_ordering_does_not_affect_price():
    assert calculate_price(['title1', 'title2', 'title3', 'title4', 'title5']) == calculate_price(['title5', 'title4', 'title3', 'title2', 'title1'])  # AC-3.3: Same titles in different order produce same price