# test_bookshop.py

from solution import calculate_basket_price

def test_empty_basket_costs_zero():
    assert calculate_basket_price([]) == 0.00  # AC-1.1: An empty basket costs 0.00

def test_single_copy_costs_base_price():
    assert calculate_basket_price(['title1']) == 8.00  # AC-1.2: A single copy costs 8.00

def test_multiple_copies_of_same_title_costs_full_price():
    assert calculate_basket_price(['title1', 'title1']) == 16.00  # AC-1.3: Two copies of the same title

def test_two_distinct_titles_discounted():
    assert calculate_basket_price(['title1', 'title2']) == 15.20  # AC-2.1: Two distinct titles cost 15.20

def test_three_distinct_titles_discounted():
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60  # AC-2.1: Three distinct titles cost 21.60

def test_four_distinct_titles_discounted():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60  # AC-2.1: Four distinct titles cost 25.60

def test_five_distinct_titles_discounted():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00  # AC-2.1: Five distinct titles cost 30.00

def test_distinct_pair_plus_duplicate():
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 23.20  # AC-3.1: Distinct pair plus a duplicate costs 15.20 + 8.00

def test_full_series_plus_one_extra():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title5']) == 38.00  # AC-3.1: Full series plus one extra copy costs 38.00

def test_two_of_every_title():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00  # AC-3.1: Two of every title costs 60.00

def test_two_four_title_sets_cheaper_than_five_plus_three():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4']) == 51.20  # AC-3.2: Two four-title sets cost 51.20

def test_five_complete_series_cost():
    assert calculate_basket_price(['title1'] * 5 + ['title2'] * 5 + ['title3'] * 5 + ['title4'] * 5 + ['title5'] * 5) == 150.00  # AC-3.4: Five complete series cost 150.00

def test_unknown_title_rejected():
    try:
        calculate_basket_price(['title6'])
    except ValueError as e:
        assert str(e) == "unknown book: title6"  # AC-4.1: Unknown title error message

def test_prices_reported_as_numeric_amounts():
    assert isinstance(calculate_basket_price(['title1', 'title2']), float)  # AC-4.2: Price is reported as a numeric amount in euros