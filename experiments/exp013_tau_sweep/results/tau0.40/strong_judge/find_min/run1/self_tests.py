import pytest
from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one, find_min_no_args, find_min_with_bounds, make_bounded_finder

# US-1: Find the smallest of my numbers

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # 1 is smaller than 34

def test_find_min_single():
    assert find_min_single(42) == 42  # Only one value, it returns itself

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # Smallest among 1, 2, 3, 4 is 1

def test_find_min_any_with_duplicates_and_negatives():
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # Smallest among the values is -5

def test_find_min_any_refuses_empty():
    # The specification states the empty candidate list is invalid
    with pytest.raises(Exception):  # Type of exception is not specified
        find_min_any()  # No candidates provided should raise an error

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # Smallest is 12

def test_find_min_at_least_one_with_required_first_value():
    assert find_min_at_least_one(3, 10, 20) == 3  # First value is the smallest

def test_find_min_at_least_one_single_value():
    assert find_min_at_least_one(7) == 7  # Only one value, it returns itself

# US-2: A variant that always refuses

def test_find_min_no_args_raises_type_error():
    with pytest.raises(TypeError) as excinfo:
        find_min_no_args()  # No arguments provided should raise a TypeError
    assert str(excinfo.value) == "Function requires arguments"

# US-3: Find the smallest within bounds

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, low=0, high=127) == 23  # Smallest within bounds is 23

def test_find_min_with_bounds_inclusive_low():
    assert find_min_with_bounds(0, 45, 0, low=0, high=127) == 0  # 0 is within bounds and is the smallest

def test_find_min_with_bounds_inclusive_high():
    assert find_min_with_bounds(127, 128, 127, low=0, high=127) == 127  # 127 is within bounds and is the only candidate

def test_find_min_with_bounds_no_candidates_within_range():
    assert find_min_with_bounds(130, 140, 150, low=0, high=127) == 127  # No candidates, returns high bound

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # Within bounds, smallest is 12