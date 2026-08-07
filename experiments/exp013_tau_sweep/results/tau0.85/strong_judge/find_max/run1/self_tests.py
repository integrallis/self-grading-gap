import pytest
from solution import find_largest, find_largest_at_least_one, find_largest_within_bounds, make_bounded_finder, always_refuses

# Test for US-1: Find the largest of my numbers

def test_find_largest_two_numbers():
    assert find_largest(1, 34) == 34  # larger of 1 and 34 is 34

def test_find_largest_single_value():
    assert find_largest(42) == 42  # single value returns itself

def test_find_largest_any_count():
    assert find_largest(1, 2, 3, 4) == 4  # largest among 1, 2, 3, 4 is 4

def test_find_largest_duplicates_and_negatives():
    assert find_largest(-5, -5, -1, -30) == -1  # largest among -5, -5, -1, -30 is -1

def test_find_largest_empty_candidate_list():
    find_largest()  # empty candidate list should be rejected

def test_find_largest_at_least_one():
    assert find_largest_at_least_one(12454, 1123, 1421, 12) == 12454  # 12454 is largest among these

def test_find_largest_at_least_one_single_value():
    assert find_largest_at_least_one(99) == 99  # single value returns itself

# Test for US-2: A variant that always refuses

def test_always_refuses():
    with pytest.raises(TypeError) as exc_info:
        always_refuses()  # should raise a TypeError with specific message
    assert str(exc_info.value) == "Function requires arguments"

# Test for US-3: Find the largest within bounds

def test_find_largest_within_bounds():
    assert find_largest_within_bounds(-54, 45, 140, low=0, high=127) == 45  # largest within bounds is 45

def test_find_largest_within_bounds_inclusive_high():
    assert find_largest_within_bounds(127, low=0, high=127) == 127  # 127 is within bounds and is the largest

def test_find_largest_within_bounds_inclusive_low():
    assert find_largest_within_bounds(0, low=0, high=127) == 0  # 0 is within bounds and is the only candidate

def test_find_largest_within_bounds_no_candidates():
    assert find_largest_within_bounds(low=0, high=127) == 0  # no candidates, return low bound

def test_find_largest_within_bounds_all_out_of_range():
    assert find_largest_within_bounds(-100, -50, low=0, high=127) == 0  # all candidates out of range, return low bound

# Test for US-4: Manufacture pre-configured bounded finders

def test_make_bounded_finder():
    bounded_finder = make_bounded_finder(0, 255)  # create a finder with bounds 0 to 255
    assert bounded_finder(-5, 12, 300) == 12  # largest within bounds is 12