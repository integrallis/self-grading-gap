# test_solution.py

from solution import compute_statistic

def test_minimum_statistic():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the minimum is -2
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "minimum")
    assert result == "-2"

def test_maximum_statistic():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the maximum is 92
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "maximum")
    assert result == "92"

def test_element_count_statistic():
    # The count of elements in the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11 is 10
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "element count")
    assert result == "10"

def test_average_statistic():
    # The average of the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11 is (1 - 1 + 2 - 2 + 6 + 9 + 15 - 2 + 92 + 11) / 10 = 13.1
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "average")
    assert result == "13.1"

def test_unrecognized_statistic():
    # Requesting an unrecognized statistic should yield empty text
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "unknown statistic")
    assert result == ""