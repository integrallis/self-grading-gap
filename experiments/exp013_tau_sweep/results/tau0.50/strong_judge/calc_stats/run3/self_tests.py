from solution import compute_statistic

def test_minimum():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the minimum is -2
    assert compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "minimum") == "-2"

def test_maximum():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the maximum is 92
    assert compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "maximum") == "92"

def test_element_count():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the element count is 10
    assert compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "element count") == "10"

def test_average():
    # For the series 1, -1, 2, -2, 6, 9, 15, -2, 92, 11, the average is 13.1
    # (Sum: 1 + (-1) + 2 + (-2) + 6 + 9 + 15 + (-2) + 92 + 11 = 131)
    # (Count: 10)
    # (Average: 131 / 10 = 13.1)
    assert compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "average") == "13.1"

def test_unrecognized_statistic():
    # An unrecognized statistic request should yield empty text
    assert compute_statistic([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], "unknown statistic") == ""