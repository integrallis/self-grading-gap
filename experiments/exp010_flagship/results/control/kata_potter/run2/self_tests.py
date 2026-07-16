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

def test_two_distinct_titles_get_discount():
    assert calculate_basket_price(['title1', 'title2']) == 15.20  # AC-2.1

def test_three_distinct_titles_get_discount():
    assert calculate_basket_price(['title1', 'title2', 'title3']) == 21.60  # AC-2.1

def test_four_distinct_titles_get_discount():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4']) == 25.60  # AC-2.1

def test_five_distinct_titles_get_discount():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5']) == 30.00  # AC-2.1

def test_basket_price_with_distinct_and_duplicate_titles():
    assert calculate_basket_price(['title1', 'title2', 'title1']) == 15.20 + 8.00  # AC-3.1

def test_full_series_plus_one_extra_copy():
    assert calculate_basket_price(['title1', 'title2', 'title3', 'title4', 'title5', 'title1']) == 38.00  # AC-3.1

def test_two_of_each_title():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4', 'title5', 'title5']) == 60.00  # AC-3.1

def test_two_four_title_sets_cost_less_than_one_five_title_set_and_one_three_title_set():
    assert calculate_basket_price(['title1', 'title1', 'title2', 'title2', 'title3', 'title3', 'title4', 'title4']) == 51.20  # AC-3.2

def test_large_basket():
    assert calculate_basket_price(['title1'] * 5 + ['title2'] * 5 + ['title3'] * 5 + ['title4'] * 5 + ['title5'] * 5) == 150.00  # AC-3.4

def test_reject_unknown_titles():
    try:
        calculate_basket_price(['title1', 'unknown_title'])
    except ValueError as e:
        assert str(e) == "unknown book: unknown_title"  # AC-4.1

def test_prices_reported_as_numeric_amounts_in_euros():
    price = calculate_basket_price(['title1', 'title2'])
    assert isinstance(price, float)  # AC-4.2
    assert price == 15.20  # Check expected value