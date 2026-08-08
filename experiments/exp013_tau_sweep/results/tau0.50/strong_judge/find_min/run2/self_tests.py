import pytest
from solution import find_min_two_numbers, find_min_single_value, find_min_any_count, find_min_at_least_one, find_min_no_arguments, find_min_with_bounds, manufacture_bounded_finder

# US-1: Find the smallest of my numbers

def test_find_min_two_numbers():
    assert find_min_two_numbers(1, 34) == 1  # 1 is smaller than 34

def test_find_min_single_value():
    assert find_min_single_value(42) == 42  # Returns the only value given

def test_find_min_any_count():
    assert find_min_any_count(1, 2, 3, 4) == 1  # The smallest is 1

def test_find_min_any_count_with_duplicates_and_negatives():
    assert find_min_any_count(-5, -5, 0, 3, -2) == -5  # The smallest is -5

def test_find_min_any_count_empty():
    with pytest.raises(ValueError): 
        find_min_any_count()  # Refusal for empty input as per AC-1.5

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # Smallest is 12

def test_find_min_at_least_one_required_first_value():
    assert find_min_at_least_one(3, 10, 20) == 3  # First value (3) is smallest

def test_find_min_at_least_one_single_value():
    assert find_min_at_least_one(99) == 99  # Returns the only value given

# US-2: A variant that always refuses

def test_find_min_no_arguments():
    with pytest.raises(TypeError) as excinfo:
        find_min_no_arguments()  # No arguments provided
    assert str(excinfo.value) == "Function requires arguments"  # Exact error message

# US-3: Find the smallest within bounds

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, low=0, high=127) == 23  # 23 is within bounds and the smallest

def test_find_min_with_bounds_inclusive_low():
    assert find_min_with_bounds(0, 1, 0, low=0, high=127) == 0  # 0 is equal to low bound and eligible

def test_find_min_with_bounds_inclusive_high():
    assert find_min_with_bounds(127, 200, 127, low=0, high=127) == 127  # 127 is equal to high bound and eligible

def test_find_min_with_bounds_nothing_in_range():
    assert find_min_with_bounds(200, 300, 400, low=0, high=127) == 127  # No candidates in range, return high bound

# US-4: Manufacture pre-configured bounded finders

def test_manufacture_bounded_finder():
    bounded_finder = manufacture_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # Smallest in the bounds is 12