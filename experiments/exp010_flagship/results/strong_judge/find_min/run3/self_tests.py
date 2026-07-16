# your complete test file
import pytest
from solution import min_two, min_one, min_any, min_any_at_least_one, min_no_args, min_within_bounds, make_bounded_finder

# US-1: Find the smallest of my numbers

def test_min_two():
    assert min_two(1, 34) == 1  # Smaller of the two
    assert min_two(34, 1) == 1  # Smaller of the two

def test_min_one():
    assert min_one(5) == 5  # Returns the single value

def test_min_any():
    assert min_any(1, 2, 3, 4) == 1  # Smallest of all supplied candidates
    assert min_any(-5, -5, 0, 3, -2) == -5  # Duplicates and negatives handled

def test_min_any_empty():
    with pytest.raises(Exception):  # Refusal for no candidates provided
        min_any()  # No candidates provided

def test_min_any_at_least_one():
    assert min_any_at_least_one(124, 1123, 1421, 12) == 12  # Includes required first value
    assert min_any_at_least_one(3, 10, 20) == 3  # Required first value wins
    assert min_any_at_least_one(5) == 5  # Accepts exactly one value

# US-2: A variant that always refuses

def test_min_no_args():
    with pytest.raises(TypeError) as exc:  # Refusal for no arguments
        min_no_args()  # No arguments provided
    assert str(exc.value) == "Function requires arguments"  # Check exact error message

# US-3: Find the smallest within bounds

def test_min_within_bounds():
    assert min_within_bounds(-54, 45, 23, low=0, high=127) == 23  # Smallest within range
    assert min_within_bounds(0, 0, 0, low=0, high=127) == 0  # Inclusive at the bottom
    assert min_within_bounds(127, 128, 127, low=0, high=127) == 127  # Inclusive at the top
    assert min_within_bounds(150, 200, 300, low=0, high=127) == 127  # No candidates in range

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # Create a finder with bounds
    assert bounded_finder(-5, 12, 13) == 12  # Returns smallest within the fixed bounds