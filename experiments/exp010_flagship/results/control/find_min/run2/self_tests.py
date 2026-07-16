# test_solution.py

from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one
from solution import find_min_no_args, find_min_within_bounds, make_bounded_finder

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # Smaller of two numbers
    assert find_min_two(34, 1) == 1  # Order doesn't matter

def test_find_min_single():
    assert find_min_single(42) == 42  # Single value returns itself

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # Smallest of several numbers
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # Handles negatives and duplicates
    with pytest.raises(ValueError) as excinfo:
        find_min_any()  # Should raise for empty candidate list
    assert str(excinfo.value) == 'At least one candidate is required'

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # First value plus others
    assert find_min_at_least_one(3, 10, 20) == 3  # First value wins
    assert find_min_at_least_one(42) == 42  # Exactly one value returns itself

def test_find_min_no_args():
    with pytest.raises(TypeError) as excinfo:
        find_min_no_args()  # Should raise type error
    assert str(excinfo.value) == 'Function requires arguments'

def test_find_min_within_bounds():
    assert find_min_within_bounds(-54, 45, 23, 0, 127) == 23  # Smallest in range
    assert find_min_within_bounds(0, 45, 0, 0, 127) == 0  # Boundary inclusive at low
    assert find_min_within_bounds(127, 45, 127, 0, 127) == 127  # Boundary inclusive at high
    assert find_min_within_bounds(200, 300, 400, 0, 127) == 127  # No candidates in range

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # Uses fixed bounds