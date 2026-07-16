from solution import compute_statistic

def test_minimum_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "minimum")
    assert result == "-2"  # The minimum of the list is -2

def test_maximum_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "maximum")
    assert result == "92"  # The maximum of the list is 92

def test_element_count_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "count")
    assert result == "10"  # The count of elements in the list is 10

def test_average_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "average")
    # The average is calculated as (1 + -1 + 2 + -2 + 6 + 9 + 15 + -2 + 92 + 11) / 10 = 13.1
    assert result == "13.1"  # The average of the list is 13.1

def test_unrecognized_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "median")
    assert result == ""  # An unrecognized statistic returns an empty string