# test_solution.py

from solution import compute_statistic

def test_compute_statistic_minimum():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = compute_statistic(numbers, "minimum")
    assert result == "-2"  # The minimum of the list is -2.

def test_compute_statistic_maximum():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = compute_statistic(numbers, "maximum")
    assert result == "92"  # The maximum of the list is 92.

def test_compute_statistic_count():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = compute_statistic(numbers, "count")
    assert result == "10"  # There are 10 elements in the list.

def test_compute_statistic_average():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = compute_statistic(numbers, "average")
    assert result == "13.1"  # The average is the sum (131) divided by count (10).

def test_compute_statistic_unrecognized_statistic():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    result = compute_statistic(numbers, "unknown_statistic")
    assert result == ""  # Unrecognized statistic should return empty text.