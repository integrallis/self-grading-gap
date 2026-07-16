from solution import compute_statistic

def test_compute_minimum():
    # Given the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the minimum is -2.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'minimum')
    assert result == "-2"

def test_compute_maximum():
    # Given the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the maximum is 92.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'maximum')
    assert result == "92"

def test_compute_element_count():
    # Given the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the count of elements is 10.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'count')
    assert result == "10"

def test_compute_average():
    # Given the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the average is (1 - 1 + 2 - 2 + 6 + 9 + 15 - 2 + 92 + 11) / 10 = 13.1.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'average')
    assert result == "13.1"

def test_unrecognized_statistic():
    # Requesting an unrecognized statistic 'median' should yield empty text.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'median')
    assert result == ""