# test_solution.py

import pytest
from solution import compute_door_states

def test_zero_doors():
    # AC-3.1: Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_door_states(0) == ([], [], "")

def test_negative_doors():
    # AC-3.2: A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    with pytest.raises(Exception) as exc_info:
        compute_door_states(-1)
    assert str(exc_info.value) == "door count must be non-negative"

def test_one_door():
    # AC-1.2: A single door ends open: the only walk toggles it once.
    # 1 door: toggled once, ends open.
    assert compute_door_states(1) == ([True], [1], "@")

def test_two_doors():
    # AC-1.3: Door 2 ends closed: it is toggled twice, by walks 1 and 2.
    # 2 doors: toggled: [True, False], open positions: [1], string: "@#"
    assert compute_door_states(2) == ([True, False], [1], "@#")

def test_three_doors():
    # 3 doors: toggled: [True, False, False], open positions: [1], string: "@##"
    assert compute_door_states(3) == ([True, False, False], [1], "@##")

def test_four_doors():
    # AC-1.1: For 4 doors, after walks, doors 1 and 4 remain open.
    # 4 doors: toggled: [True, False, False, True], open positions: [1, 4], string: "@##@"
    assert compute_door_states(4) == ([True, False, False, True], [1, 4], "@##@")

def test_fifty_doors():
    # AC-1.1: For 50 doors, the open positions are perfect squares: [1, 4, 9, 16, 25, 36, 49]
    # 50 doors: toggled: [True, False, False, True, False, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False, False, False, True, False]
    open_positions = [i**2 for i in range(1, 8)] # [1, 4, 9, 16, 25, 36, 49]
    expected_list = [i in open_positions for i in range(1, 51)]
    expected_string = "".join("@" if i in open_positions else "#" for i in range(1, 51))
    
    assert compute_door_states(50) == (expected_list, open_positions, expected_string)

def test_ten_doors():
    # AC-1.1: 10 doors leave doors 1, 4, 9 open.
    # 10 doors: toggled: [True, False, False, True, False, False, False, False, True, False], open positions: [1, 4, 9], string: "@##@####@#"
    assert compute_door_states(10) == ([True, False, False, True, False, False, False, False, True, False], [1, 4, 9], "@##@####@#")

def test_hundred_doors():
    # AC-1.1: 100 doors leave doors 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 open.
    # 100 doors: the open positions are perfect squares: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    open_positions = [i**2 for i in range(1, 11)]
    expected_list = [i in open_positions for i in range(1, 101)]
    expected_string = "".join("@" if i in open_positions else "#" for i in range(1, 101))
    
    assert compute_door_states(100) == (expected_list, open_positions, expected_string)