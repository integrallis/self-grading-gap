from solution import compute_statistic

def test_minimum_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "minimum")
    assert result == "-2"  # Minimum of the list is -2.

def test_maximum_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "maximum")
    assert result == "92"  # Maximum of the list is 92.

def test_element_count_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "count")
    assert result == "10"  # There are 10 elements in the list.

def test_average_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "average")
    # Average = (1 - 1 + 2 - 2 + 6 + 9 + 15 - 2 + 92 + 11) / 10 = 13.1
    assert result == "13.1"  # The average is 13.1.

def test_minimum_statistic_non_canonical():
    result = compute_statistic([3, 5, 1, 8, -4], "minimum")
    assert result == "-4"  # Minimum of the list is -4.

def test_maximum_statistic_non_canonical():
    result = compute_statistic([3, 5, 1, 8, -4], "maximum")
    assert result == "8"  # Maximum of the list is 8.

def test_element_count_statistic_non_canonical():
    result = compute_statistic([3, 5, 1, 8, -4], "count")
    assert result == "5"  # There are 5 elements in the list.

def test_average_statistic_non_canonical():
    result = compute_statistic([3, 5, 1, 8, -4], "average")
    # Average = (3 + 5 + 1 + 8 - 4) / 5 = 2.6
    assert result == "2.6"  # The average is 2.6.

def test_unrecognized_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "unknown_statistic")
    assert result == ""  # Unrecognized statistic should yield empty text.