from solution import statistic_reporter

def test_minimum():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    statistic = "minimum"
    expected = "-2"  # The minimum value in the list
    assert statistic_reporter(numbers, statistic) == expected

def test_maximum():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    statistic = "maximum"
    expected = "92"  # The maximum value in the list
    assert statistic_reporter(numbers, statistic) == expected

def test_element_count():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    statistic = "element count"
    expected = "10"  # The count of elements in the list
    assert statistic_reporter(numbers, statistic) == expected

def test_average():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    statistic = "average"
    expected = "13.1"  # The average is computed as (1 + -1 + 2 + -2 + 6 + 9 + 15 + -2 + 92 + 11) / 10 = 13.1
    assert statistic_reporter(numbers, statistic) == expected

def test_unrecognized_statistic():
    numbers = [1, -1, 2, -2, 6, 9, 15, -2, 92, 11]
    statistic = "unknown statistic"
    expected = ""  # An unrecognized statistic should yield empty text
    assert statistic_reporter(numbers, statistic) == expected

def test_parameterized_statistics():
    numbers = [1, 2, 3, 8]
    assert statistic_reporter(numbers, "minimum") == "1"  # The minimum value in the list
    assert statistic_reporter(numbers, "maximum") == "8"  # The maximum value in the list
    assert statistic_reporter(numbers, "element count") == "4"  # The count of elements in the list
    expected_average = (1 + 2 + 3 + 8) / 4  # Average = (1 + 2 + 3 + 8) / 4 = 3.5
    assert statistic_reporter(numbers, "average") == "3.5"  # The average as a decimal