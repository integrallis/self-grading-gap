import pytest
from solution import find_largest, find_largest_any, find_largest_at_least_one, find_largest_within_bounds, make_bounded_finder, always_refuses

# US-1: Find the largest of my numbers

def test_find_largest_two_numbers():
    assert find_largest(1, 34) == 34  # 34 is larger than 1

def test_find_largest_single_value():
    assert find_largest(42) == 42  # Only one value is given, return it

def test_find_largest_any_count():
    assert find_largest_any(1, 2, 3, 4) == 4  # Largest of 1, 2, 3, 4 is 4

def test_find_largest_any_count_duplicates_negatives():
    assert find_largest_any(-5, -5, -1, -30) == -1  # Largest is -1

def test_find_largest_any_count_empty():
    with pytest.raises(ValueError):  # Expecting a ValueError for empty input
        find_largest_any()

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is the largest

def test_find_largest_at_least_one_single_value():
    assert find_largest_at_least_one(100) == 100  # Single value should return itself

# US-2: A variant that always refuses

def test_always_refuses_no_arguments():
    with pytest.raises(TypeError) as excinfo:
        always_refuses()
    assert str(excinfo.value) == "Function requires arguments"  # Check error message

# US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, 0, 127) == 45  # 45 is the largest within bounds

def test_find_largest_within_bounds_inclusive_high():
    assert find_largest_within_bounds(127, 0, 127) == 127  # 127 is within bounds

def test_find_largest_within_bounds_inclusive_low():
    assert find_largest_within_bounds(0, 0, 127) == 0  # 0 is the only candidate and is within bounds

def test_find_largest_within_bounds_no_candidates():
    assert find_largest_within_bounds(100, 200, 150) == 100  # No candidates, return low bound

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 300) == 12  # Largest within bounds 0 to 255 is 12