from solution import compute_statistic

def test_request_minimum():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "minimum")
    assert result == "-2"  # The minimum of the list is -2

def test_request_maximum():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "maximum")
    assert result == "92"  # The maximum of the list is 92

def test_request_element_count():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "element count")
    assert result == "10"  # There are 10 elements in the list

def test_request_average():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "average")
    average = sum([1, -1, 2, -2, 6, 9, 15, -2, 92, 11]) / 10  # Compute average
    assert result == str(average)  # The average is 13.1, delivered as text

def test_request_unrecognized_statistic():
    result = compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "median")
    assert result == ""  # Unrecognized statistic yields empty text

def test_request_minimum_noncanonical():
    result = compute_statistic([7, -4, 7, 0], "minimum")
    assert result == "-4"  # The minimum of the list is -4

def test_request_maximum_noncanonical():
    result = compute_statistic([7, -4, 7, 0], "maximum")
    assert result == "7"  # The maximum of the list is 7

def test_request_element_count_noncanonical():
    result = compute_statistic([7, -4, 7, 0], "element count")
    assert result == "4"  # There are 4 elements in the list

def test_request_average_noncanonical():
    result = compute_statistic([7, -4, 7, 0], "average")
    average = sum([7, -4, 7, 0]) / 4  # Compute average
    assert result == str(average)  # The average is 2.5, delivered as text