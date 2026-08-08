# test_solution.py

import pytest
from solution import (
    max_of_two,
    max_of_one,
    max_of_any,
    max_of_at_least_one,
    always_refuses,
    max_within_bounds,
    make_bounded_finder
)

# US-1: Find the largest of my numbers

def test_max_of_two():
    assert max_of_two(1, 34) == 34  # larger of the two numbers
    assert max_of_two(-5, -1) == -1  # larger of the two negative numbers

def test_max_of_one():
    assert max_of_one(42) == 42  # single value returns itself

def test_max_of_any():
    assert max_of_any(1, 2, 3, 4) == 4  # largest of multiple values
    assert max_of_any(-5, -5, -1, -30) == -1  # largest among negatives
    # The specification says it refuses empty input, but does not specify how,
    # so we just check if it raises an error without specifying the type.
    with pytest.raises(Exception):  # expects an exception for empty input
        max_of_any() 

def test_max_of_at_least_one():
    assert max_of_at_least_one(12454, 1123, 1421, 12) == 12454  # first value can be the largest
    assert max_of_at_least_one(42) == 42  # single value returns itself

# US-2: A variant that always refuses

def test_always_refuses():
    with pytest.raises(TypeError) as excinfo:  # expects TypeError when called
        always_refuses()
    assert str(excinfo.value) == "Function requires arguments"  # exact error message

# US-3: Find the largest within bounds

def test_max_within_bounds():
    assert max_within_bounds(-54, 45, 140, low=0, high=127) == 45  # largest within range
    assert max_within_bounds(127, low=0, high=127) == 127  # largest equal to high bound
    assert max_within_bounds(0, low=0, high=127) == 0  # largest equal to low bound
    assert max_within_bounds(-10, -20, -30, low=0, high=127) == 0  # no in-range candidates, return low bound

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # create finder with bounds
    assert bounded_finder(-5, 12, 300) == 12  # finds largest within bounds