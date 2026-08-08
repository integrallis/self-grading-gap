import pytest
from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one, find_min_no_args, find_min_with_bounds, make_bounded_finder

# US-1: Find the smallest of my numbers

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # 1 is smaller than 34

def test_find_min_single():
    assert find_min_single(42) == 42  # returns the only value given

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # smallest is 1

def test_find_min_any_with_duplicates_and_negatives():
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # smallest is -5

def test_find_min_any_empty():
    with pytest.raises(Exception):  # should raise an error for empty candidate list
        find_min_any()  

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # smallest is 12

def test_find_min_at_least_one_with_required_first_value():
    assert find_min_at_least_one(3, 10, 20) == 3  # first value is the smallest

def test_find_min_at_least_one_with_one_value():
    assert find_min_at_least_one(42) == 42  # returns the only value given


# US-2: A variant that always refuses

def test_find_min_no_args():
    with pytest.raises(TypeError):  # should raise a TypeError
        find_min_no_args()  


# US-3: Find the smallest within bounds

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, low=0, high=127) == 23  # 23 is within bounds

def test_find_min_with_bounds_inclusive_low():
    assert find_min_with_bounds(0, 45, 0, low=0, high=127) == 0  # 0 is eligible and wins

def test_find_min_with_bounds_inclusive_high():
    assert find_min_with_bounds(127, 150, 127, low=0, high=127) == 127  # 127 is eligible and wins

def test_find_min_with_bounds_no_valid_candidates():
    assert find_min_with_bounds(200, 300, 400, low=0, high=127) == 127  # no candidates in range, return high bound


# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # 12 is the smallest within bounds