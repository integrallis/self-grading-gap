from solution import statistic_reporter

def test_statistic_reporter_minimum():
    # For the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the minimum is -2
    assert statistic_reporter([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'minimum') == "-2"

def test_statistic_reporter_maximum():
    # For the list [3, 5, 1, 10, 0], the maximum is 10
    assert statistic_reporter([3, 5, 1, 10, 0], 'maximum') == "10"

def test_statistic_reporter_element_count():
    # For the list [4, 8, 15, 16, 23, 42], the element count is 6
    assert statistic_reporter([4, 8, 15, 16, 23, 42], 'element count') == "6"

def test_statistic_reporter_average():
    # For the list [1, -1, 2, -2, 6, 9, 15, -2, 92, 11], the average is (1 - 1 + 2 - 2 + 6 + 9 + 15 - 2 + 92 + 11) / 10 = 131 / 10 = 13.1
    assert statistic_reporter([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'average') == "13.1"

def test_statistic_reporter_unrecognized_statistic():
    # An unrecognized statistic selector yields an empty text
    assert statistic_reporter([1, -1, 2, -2, 6, 9, 15, -2, 92, 11], 'unknown statistic') == ""