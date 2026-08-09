import pytest
from solution import find_max, find_max_single, find_max_any_count, find_max_at_least_one
from solution import find_max_in_bounds, make_bounded_finder, find_max_no_args

# US-1: Find the largest of my numbers

def test_find_max_two_numbers():
    assert find_max(1, 34) == 34  # 34 is larger than 1

def test_find_max_single_value():
    assert find_max_single(42) == 42  # Only one value, returns 42

def test_find_max_any_count():
    assert find_max_any_count(1, 2, 3, 4) == 4  # Largest is 4

def test_find_max_any_count_with_negatives():
    assert find_max_any_count(-5, -5, -1, -30) == -1  # Largest is -1

def test_find_max_any_count_empty():
    with pytest.raises(TypeError):  # Expecting some type of error for empty input
        find_max_any_count()  # No candidates provided

def test_find_max_at_least_one_with_multiple_values():
    assert find_max_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is the largest

def test_find_max_at_least_one_with_one_value():
    assert find_max_at_least_one(99) == 99  # Only one value, returns 99


# US-2: A variant that always refuses

def test_find_max_no_args():
    with pytest.raises(TypeError) as e:  # Expecting a TypeError
        find_max_no_args()  # No arguments provided
    assert str(e.value) == "Function requires arguments"  # Exact error message


# US-3: Find the largest within bounds

def test_find_max_in_bounds():
    assert find_max_in_bounds(-54, 45, 140, low=0, high=127) == 45  # Largest within bounds is 45

def test_find_max_in_bounds_inclusive_high():
    assert find_max_in_bounds(127, low=0, high=127) == 127  # 127 is equal to the high bound

def test_find_max_in_bounds_inclusive_low():
    assert find_max_in_bounds(0, low=0, high=127) == 0  # 0 is equal to the low bound

def test_find_max_in_bounds_no_candidates():
    assert find_max_in_bounds(10, low=0, high=5) == 0  # No candidates, return the low bound


# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 300) == 12  # Largest within bounds is 12