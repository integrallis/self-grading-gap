# test_solution.py

from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one, find_min_no_args, find_min_with_bounds, make_bounded_finder

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # smaller one is returned
    assert find_min_two(34, 1) == 1  # smaller one is returned

def test_find_min_single():
    assert find_min_single(42) == 42  # returns the one value it is given

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # smallest of all supplied candidates
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # handles duplicates and negative values
    assert find_min_any() ==  # raises an error for empty candidate list

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # smallest among all of them
    assert find_min_at_least_one(3, 10, 20) == 3  # required first value participates in comparison
    assert find_min_at_least_one(42) == 42  # accepts exactly one value and returns it

def test_find_min_no_args():
    import pytest
    with pytest.raises(TypeError) as excinfo:
        find_min_no_args()  # calling raises a type error
    assert str(excinfo.value) == "Function requires arguments"  # error message matches

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, 0, 127) == 23  # smallest candidate within the range
    assert find_min_with_bounds(0, 45, 0, 0, 127) == 0  # candidate equal to the low bound is eligible
    assert find_min_with_bounds(127, 128, 0, 0, 127) == 127  # candidate equal to the high bound is eligible
    assert find_min_with_bounds(200, 300, 0, 0, 127) == 127  # no candidate within the range

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # produces a callable finder
    assert bounded_finder(-5, 12, 13) == 12  # returns smallest of candidates within fixed bounds