import pytest
from solution import find_min_two, find_min_single, find_min_any, find_min_at_least_one, find_min_no_args, find_min_with_bounds, create_bounded_finder

# Test for US-1: Find the smallest of my numbers

def test_find_min_two():
    assert find_min_two(1, 34) == 1  # AC-1.1
    assert find_min_two(34, 1) == 1  # AC-1.1

def test_find_min_single():
    assert find_min_single(3) == 3  # AC-1.2

def test_find_min_any():
    assert find_min_any(1, 2, 3, 4) == 1  # AC-1.3
    assert find_min_any(-5, -5, 0, 3, -2) == -5  # AC-1.4
    with pytest.raises(Exception):  # AC-1.5, refusal for empty candidate list
        find_min_any()  # should refuse

def test_find_min_at_least_one():
    assert find_min_at_least_one(124, 1123, 1421, 12) == 12  # AC-1.6
    assert find_min_at_least_one(3, 10, 20) == 3  # AC-1.7
    assert find_min_at_least_one(42) == 42  # AC-1.8

# Test for US-2: A variant that always refuses

def test_find_min_no_args():
    with pytest.raises(TypeError) as exc_info:  # AC-2.1
        find_min_no_args()
    assert str(exc_info.value) == "Function requires arguments"  # AC-2.2

# Test for US-3: Find the smallest within bounds

def test_find_min_with_bounds():
    assert find_min_with_bounds(-54, 45, 23, low=0, high=127) == 23  # AC-3.1
    assert find_min_with_bounds(0, 0, 0, low=0, high=127) == 0  # AC-3.2
    assert find_min_with_bounds(-1, 127, 200, low=0, high=127) == 127  # AC-3.3
    assert find_min_with_bounds(-1, -2, -3, low=0, high=0) == 0  # AC-3.4

# Test for US-4: Manufacture pre-configured bounded finders

def test_create_bounded_finder():
    bounded_finder = create_bounded_finder(0, 255)
    assert bounded_finder(-5, 12, 13) == 12  # AC-4.2