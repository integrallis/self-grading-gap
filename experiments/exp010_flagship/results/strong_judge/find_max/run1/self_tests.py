# test_solution.py

import pytest
from solution import find_largest
from solution import find_largest_any
from solution import find_largest_at_least_one
from solution import find_largest_within_bounds
from solution import create_bounded_finder
from solution import always_refuse

def test_find_largest_two_numbers():
    assert find_largest(1, 34) == 34  # larger of 1 and 34
    assert find_largest(-5, -1) == -1  # larger of -5 and -1

def test_find_largest_single_value():
    assert find_largest(42) == 42  # single value returns itself

def test_find_largest_any_count():
    assert find_largest_any(1, 2, 3, 4) == 4  # largest among 1, 2, 3, 4
    assert find_largest_any(-5, -5, -1, -30) == -1  # largest among negatives
    with pytest.raises(TypeError):
        find_largest_any()  # should raise an error for empty input

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # first value wins
    assert find_largest_at_least_one(42) == 42  # single value returns itself

def test_always_refuse():
    with pytest.raises(TypeError) as exc:
        always_refuse()  # should raise a TypeError
    assert str(exc.value) == "Function requires arguments"  # exact error message

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, low=0, high=127) == 45  # largest in range
    assert find_largest_within_bounds(127, low=0, high=127) == 127  # 127 is eligible and largest
    assert find_largest_within_bounds(0, low=0, high=127) == 0  # 0 is the only in-range candidate
    assert find_largest_within_bounds(200, 300, 400, low=0, high=127) == 0  # no candidates in range

def test_create_bounded_finder():
    bounded_finder = create_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 300) == 12  # largest in bounds