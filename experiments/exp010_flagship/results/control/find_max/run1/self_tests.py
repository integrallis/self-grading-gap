import pytest
from solution import (
    find_largest_two,
    find_largest_single,
    find_largest_any,
    find_largest_at_least_one,
    find_largest_within_bounds,
    make_bounded_finder,
    always_refuses
)

# US-1: Find the largest of my numbers

def test_find_largest_two():
    assert find_largest_two(1, 34) == 34  # 34 is larger than 1

def test_find_largest_single():
    assert find_largest_single(42) == 42  # Single value returns itself

def test_find_largest_any():
    assert find_largest_any(1, 2, 3, 4) == 4  # Largest of 1, 2, 3, 4 is 4

def test_find_largest_any_with_duplicates_and_negatives():
    assert find_largest_any(-5, -5, -1, -30) == -1  # -1 is the largest

def test_find_largest_any_empty():
    with pytest.raises(ValueError) as excinfo:
        find_largest_any()  # An empty candidate list should raise an error
    assert str(excinfo.value) == "No candidates provided"

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is the largest

def test_find_largest_at_least_one_single_value():
    assert find_largest_at_least_one(100) == 100  # Single value returns itself

# US-2: A variant that always refuses

def test_always_refuses():
    with pytest.raises(TypeError) as excinfo:
        always_refuses()  # Should raise TypeError when called without arguments
    assert str(excinfo.value) == "Function requires arguments"  # Check the error message

# US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, 0, 127) == 45  # 45 is the largest within bounds

def test_find_largest_within_bounds_inclusive_high():
    assert find_largest_within_bounds(127, 0, 127) == 127  # 127 is within bounds and is the largest

def test_find_largest_within_bounds_inclusive_low():
    assert find_largest_within_bounds(0, 0, 127) == 0  # 0 is within bounds and is the only candidate

def test_find_largest_within_bounds_no_candidates():
    assert find_largest_within_bounds(100, 200, 300) == 100  # No candidates, return the low bound

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # Create a bounded finder for 0 to 255
    assert bounded_finder(-5, 12, 300) == 12  # Largest within bounds is 12