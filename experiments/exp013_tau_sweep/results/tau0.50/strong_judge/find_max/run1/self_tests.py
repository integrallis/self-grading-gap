import pytest
from solution import (
    find_largest_two,
    find_largest_single,
    find_largest_any_count,
    find_largest_at_least_one,
    find_largest_within_bounds,
    create_bounded_finder,
    always_refuses
)

# US-1: Find the largest of my numbers

def test_find_largest_two():
    assert find_largest_two(1, 34) == 34  # Larger of two numbers
    assert find_largest_two(-5, -1) == -1  # Larger of two negative numbers

def test_find_largest_single():
    assert find_largest_single(42) == 42  # Returns the single value given

def test_find_largest_any_count():
    assert find_largest_any_count(1, 2, 3, 4) == 4  # Largest of multiple numbers
    assert find_largest_any_count(-5, -5, -1, -30) == -1  # Handles duplicates and negatives
    # Empty candidate list should refuse input
    assert find_largest_any_count() is None  # Should refuse input without raising an exception

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # First value wins
    assert find_largest_at_least_one(100) == 100  # Accepts exactly one value

# US-2: A variant that always refuses

def test_always_refuses():
    assert always_refuses() is None  # Should refuse input without raising an exception
    with pytest.raises(TypeError) as excinfo:  # Any argument should raise a TypeError
        always_refuses(1)
    assert str(excinfo.value) == "Function requires arguments"  # Check error message

# US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, low=0, high=127) == 45  # Largest within bounds
    assert find_largest_within_bounds(127, low=0, high=127) == 127  # High bound is inclusive
    assert find_largest_within_bounds(0, low=0, high=127) == 0  # Low bound is inclusive
    assert find_largest_within_bounds(-10, -20, -30, low=5, high=15) == 5  # No candidates in range return low bound

# US-4: Manufacture pre-configured bounded finders

def test_create_bounded_finder():
    bounded_finder = create_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 300) == 12  # Returns largest within fixed bounds