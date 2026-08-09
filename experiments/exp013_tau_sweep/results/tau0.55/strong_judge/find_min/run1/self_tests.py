import pytest
from solution import min_two, min_single, min_any, min_any_at_least_one, min_no_argument, min_within_bounds, make_bounded_finder

# US-1: Find the smallest of my numbers

def test_min_two():
    assert min_two(1, 34) == 1  # 1 is smaller than 34
    assert min_two(34, 1) == 1  # 1 is smaller than 34

def test_min_single():
    assert min_single(5) == 5  # Only one value is provided

def test_min_any():
    assert min_any(1, 2, 3, 4) == 1  # 1 is the smallest among the candidates
    assert min_any(5, 5, -5, 0, 3, -2) == -5  # -5 is the smallest among the candidates
    # Just check that it raises an error for empty input, no specific type requirement
    with pytest.raises(Exception):  # Expecting some error for empty input
        min_any()

def test_min_any_at_least_one():
    assert min_any_at_least_one(124, 1123, 1421, 12) == 12  # 12 is the smallest among the candidates
    assert min_any_at_least_one(3, 10, 20) == 3  # 3 is the smallest among the candidates
    assert min_any_at_least_one(5) == 5  # Only one value is provided

# US-2: A variant that always refuses

def test_min_no_argument():
    with pytest.raises(TypeError) as excinfo:
        min_no_argument()
    assert str(excinfo.value) == "Function requires arguments"  # Check the exact error message

# US-3: Find the smallest within bounds

def test_min_within_bounds():
    assert min_within_bounds(-54, 45, 23, low=0, high=127) == 23  # 23 is within the bounds and is the smallest
    assert min_within_bounds(0, 0, 1, 2, 3, low=0, high=127) == 0  # 0 is within the bounds and is the smallest
    assert min_within_bounds(128, 256, 300, low=0, high=255) == 255  # No candidates within bounds, return high bound
    assert min_within_bounds(-1, 127, 128, low=0, high=127) == 127  # 127 is equal to high and the only in-range candidate

# US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # Create a finder with bounds 0 to 255
    assert bounded_finder(-5, 12, 13) == 12  # 12 is the smallest within the bounds