import pytest
from solution import compute_final_states  # Assuming this will be the function name

# US-1: Compute the final door states
def test_one_door():
    # 1 door: toggled once, should be open
    assert compute_final_states(1) == [True]  # Open

def test_two_doors():
    # 2 doors: door 1 toggled once (open), door 2 toggled twice (closed)
    assert compute_final_states(2) == [True, False]  # Open, Closed

def test_ten_doors():
    # 10 doors: perfect squares are 1, 4, 9; hence the result should reflect that
    assert compute_final_states(10) == [True, False, False, True, False, False, False, False, True, False]

def test_fifty_doors():
    # 50 doors: perfect squares are 1, 4, 9, 16, 25, 36, 49
    expected_result = [True, False, False, True, False, False, False, False, True, False,
                       False, False, True, False, False, False, True, False, False, False,
                       False, False, False, False, False, False, False, False, True, False,
                       False, False, False, False, False, False, False, False, False, False,
                       False, False, False, False, True, False]
    assert compute_final_states(50) == expected_result

def test_one_hundred_doors():
    # 100 doors: perfect squares are 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    expected_result = [True, False, False, True, False, False, False, False, True, False] + [False] * 90
    assert compute_final_states(100) == expected_result

# US-2: Report the outcome in three forms
def test_final_state_list():
    # 10 doors: open/closed indicators
    assert compute_final_states(10) == [True, False, False, True, False, False, False, False, True, False]

def test_final_state_positions():
    # 10 doors: positions of open doors are 1, 4, 9
    assert compute_final_states(10, return_type='positions') == [1, 4, 9]

def test_final_state_string():
    # 10 doors: string representation
    assert compute_final_states(10, return_type='string') == "@##@####@#"

# US-3: Handle edge counts
def test_zero_doors():
    # 0 doors should yield empty states
    assert compute_final_states(0) == []  # Empty state list
    assert compute_final_states(0, return_type='positions') == []  # Empty open positions
    assert compute_final_states(0, return_type='string') == ""  # Empty string

def test_negative_doors():
    # Negative door count should raise an error with the exact message
    with pytest.raises(Exception, match=r"^door count must be non-negative$"):
        compute_final_states(-1)