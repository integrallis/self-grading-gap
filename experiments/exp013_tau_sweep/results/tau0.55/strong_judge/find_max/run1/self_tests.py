# test_solution.py

import pytest
from solution import (
    find_largest_two,
    find_largest_single,
    find_largest_any,
    find_largest_at_least_one,
    find_largest_within_bounds,
    make_bounded_finder,
    always_refuses,
)

# US-1: Find the largest of my numbers

def test_find_largest_two():
    assert find_largest_two(1, 34) == 34  # Larger of 1 and 34 is 34
    assert find_largest_two(-5, -1) == -1  # Larger of -5 and -1 is -1

def test_find_largest_single():
    assert find_largest_single(42) == 42  # Single value is 42

def test_find_largest_any():
    assert find_largest_any(1, 2, 3, 4) == 4  # Largest of 1, 2, 3, 4 is 4
    assert find_largest_any(-5, -5, -1, -30) == -1  # Largest of -5, -5, -1, -30 is -1
    # Should raise an error for empty input (exact exception type is not specified)
    with pytest.raises(Exception):  # Expecting some exception for empty input
        find_largest_any()

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is the largest
    assert find_largest_at_least_one(42) == 42  # Single value is 42

# US-2: A variant that always refuses

def test_always_refuses():
    with pytest.raises(TypeError) as excinfo:  # Expecting TypeError
        always_refuses()
    assert str(excinfo.value) == "Function requires arguments"  # Check the error message

# US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, low=0, high=127) == 45  # Largest within 0 to 127 is 45
    assert find_largest_within_bounds(127, 0, low=0, high=127) == 127  # 127 is eligible (equal to high bound)
    assert find_largest_within_bounds(0, 0, low=0, high=127) == 0  # 0 is eligible (equal to low bound)
    assert find_largest_within_bounds(-10, -20, low=0, high=10) == 0  # No candidates, return low bound

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # Create a bounded finder with bounds 0 to 255
    assert bounded_finder(-5, 12, 300) == 12  # Largest within bounds 0 to 255 is 12