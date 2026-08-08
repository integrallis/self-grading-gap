import pytest
from solution import find_largest_two, find_largest_single, find_largest_any, find_largest_at_least_one
from solution import find_largest_within_bounds, create_bounded_finder, always_refuse

# US-1: Find the largest of my numbers

def test_find_largest_two():
    assert find_largest_two(1, 34) == 34  # larger of the two
    assert find_largest_two(-5, -1) == -1  # larger negative value

def test_find_largest_single():
    assert find_largest_single(5) == 5  # single value returned

def test_find_largest_any():
    assert find_largest_any(1, 2, 3, 4) == 4  # largest among several
    assert find_largest_any(-5, -5, -1, -30) == -1  # handle duplicates and negatives

def test_find_largest_any_empty():
    with pytest.raises(Exception):  # should refuse empty candidate list
        find_largest_any()  # no specific exception type or message defined in the specification

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # first value is the largest
    assert find_largest_at_least_one(5) == 5  # single value accepted

# US-2: A variant that always refuses

def test_always_refuse():
    with pytest.raises(TypeError) as excinfo:
        always_refuse()  # should raise a type error
    assert str(excinfo.value) == "Function requires arguments"  # exact error message

# US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, low=0, high=127) == 45  # largest in range
    assert find_largest_within_bounds(127, 0, 127, low=0, high=127) == 127  # inclusive high bound
    assert find_largest_within_bounds(-1, 0, 128, low=0, high=127) == 0  # inclusive low bound with 0 as the only in-range candidate
    assert find_largest_within_bounds(200, 300, 400, low=0, high=127) == 0  # no candidates in range return low bound

# US-4: Manufacture pre-configured bounded finders

def test_create_bounded_finder():
    bounded_finder = create_bounded_finder(0, 255)  # create a finder with fixed bounds
    assert bounded_finder(-5, 12, 300) == 12  # largest within fixed bounds