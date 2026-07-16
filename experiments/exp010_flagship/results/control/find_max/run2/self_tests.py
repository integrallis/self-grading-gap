import pytest
from solution import find_max, find_max_single, find_max_any, find_max_at_least_one
from solution import find_max_within_bounds, manufacture_bounded_finder, always_refuses

# US-1: Find the largest of my numbers

def test_find_max_two_numbers():
    assert find_max(1, 34) == 34  # 34 is larger than 1

def test_find_max_single_value():
    assert find_max_single(42) == 42  # Single value returns itself

def test_find_max_any_count():
    assert find_max_any(1, 2, 3, 4) == 4  # 4 is the largest

def test_find_max_any_count_with_negatives():
    assert find_max_any(-5, -5, -1, -30) == -1  # -1 is the largest

def test_find_max_any_count_empty():
    with pytest.raises(ValueError):  # Expecting a ValueError for empty input
        find_max_any()

def test_find_max_at_least_one_with_multiple_values():
    assert find_max_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is largest

def test_find_max_at_least_one_with_one_value():
    assert find_max_at_least_one(100) == 100  # Single value returns itself

# US-2: A variant that always refuses

def test_always_refuses_no_arguments():
    with pytest.raises(TypeError) as exc_info:  # Expecting a TypeError
        always_refuses()
    assert str(exc_info.value) == "Function requires arguments"  # Exact error message

# US-3: Find the largest within bounds

def test_find_max_within_bounds():
    assert find_max_within_bounds(-54, 45, 140, 0, 127) == 45  # 45 is largest within bounds

def test_find_max_within_bounds_inclusive_high():
    assert find_max_within_bounds(127, 0, 127) == 127  # 127 is equal to high bound

def test_find_max_within_bounds_inclusive_low():
    assert find_max_within_bounds(0, 0, 127) == 0  # 0 is equal to low bound

def test_find_max_within_bounds_no_candidates():
    assert find_max_within_bounds(100, 200, 150) == 100  # No candidates, return low bound

# US-4: Manufacture pre-configured bounded finders

def test_manufacture_bounded_finder():
    bounded_finder = manufacture_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 300) == 12  # 12 is the largest within bounds