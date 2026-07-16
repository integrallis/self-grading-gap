import pytest
from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one, find_min_no_arg, find_min_with_bounds, manufacture_bounded_finder

# US-1: Find the smallest of my numbers

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # 1 is smaller than 34

def test_find_min_single():
    assert find_min_single(42) == 42  # single value returns itself

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # smallest among the candidates is 1

def test_find_min_any_with_duplicates_and_negatives():
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # -5 is the smallest

def test_find_min_any_empty():
    with pytest.raises(ValueError) as excinfo:
        find_min_any()  # should raise ValueError for empty input
    assert str(excinfo.value) == "No candidates provided"

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # smallest is 12

def test_find_min_at_least_one_with_required_value():
    assert find_min_at_least_one(3, 10, 20) == 3  # 3 is the smallest

def test_find_min_at_least_one_with_single_value():
    assert find_min_at_least_one(42) == 42  # returns the single value

# US-2: A variant that always refuses

def test_find_min_no_arg():
    with pytest.raises(TypeError) as excinfo:
        find_min_no_arg()  # should raise TypeError
    assert str(excinfo.value) == "Function requires arguments"

# US-3: Find the smallest within bounds

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, 0, 127) == 23  # 23 is within bounds

def test_find_min_with_bounds_inclusive_low():
    assert find_min_with_bounds(0, 45, 0, 0, 127) == 0  # 0 is equal to low bound

def test_find_min_with_bounds_inclusive_high():
    assert find_min_with_bounds(127, 200, 127, 0, 127) == 127  # 127 is equal to high bound

def test_find_min_with_bounds_no_candidates():
    assert find_min_with_bounds(130, 200, 100, 0, 127) == 127  # no candidates in range, return high bound

# US-4: Manufacture pre-configured bounded finders

def test_manufacture_bounded_finder():
    bounded_finder = manufacture_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # 12 is the smallest within bounds