# test_statistics.py

from solution import compute_statistic

def test_requesting_minimum():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the minimum is -2.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'minimum')
    assert result == "-2"

def test_requesting_maximum():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the maximum is 92.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'maximum')
    assert result == "92"

def test_requesting_element_count():
    # There are 10 elements in the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'count')
    assert result == "10"

def test_requesting_average():
    # The average of the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11 is (1 - 1 + 2 - 2 + 6 + 9 + 15 - 2 + 92 + 11) / 10 = 13.1
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'average')
    assert result == "13.1"

def test_requesting_unrecognised_statistic():
    # An unrecognized statistic request should yield an empty text result.
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'unknown_statistic')
    assert result == ""