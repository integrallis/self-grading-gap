import pytest
from solution import compute_door_states

def test_zero_doors():
    # AC-3.1: Zero doors yield an empty state list, open positions, and string
    assert compute_door_states(0) == ([], [], "")

def test_negative_doors():
    # AC-3.2: A negative door count is rejected as an error with the exact message
    with pytest.raises(Exception) as exc_info:
        compute_door_states(-1)
    assert str(exc_info.value) == "door count must be non-negative"

def test_one_door():
    # AC-1.2: For 1 door, it ends open after one walk
    # 1 door is toggled once, so it remains open
    assert compute_door_states(1) == ([], [1], "@")

def test_two_doors():
    # AC-1.3: For 2 doors, door 2 ends closed
    # Door 1 is toggled once (open), Door 2 is toggled twice (closed)
    assert compute_door_states(2) == ([], [1], "@#")

def test_three_doors():
    # For 3 doors, only door 1 ends open (1 is a perfect square)
    assert compute_door_states(3) == ([], [1], "@##")

def test_ten_doors():
    # AC-1.1 example: for 10 doors, doors 1, 4, 9 remain open
    # Perfect squares up to 10 are 1, 4, 9
    assert compute_door_states(10) == ([], [1, 4, 9], "@##@####@#")

def test_fifty_doors():
    # For 50 doors, perfect squares up to 49 remain open: 1, 4, 9, 16, 25, 36, 49
    # The corresponding state list is:
    # 1 (open), 2 (closed), 3 (closed), 4 (open), 5 (closed), 6 (closed), 7 (closed), 8 (closed), 
    # 9 (open), 10 (closed), 11 (closed), 12 (closed), 13 (closed), 14 (closed), 15 (closed), 
    # 16 (open), 17 (closed), 18 (closed), 19 (closed), 20 (closed), 21 (closed), 
    # 22 (closed), 23 (closed), 24 (closed), 25 (open), 26 (closed), 27 (closed), 
    # 28 (closed), 29 (closed), 30 (closed), 31 (closed), 32 (closed), 33 (closed), 
    # 34 (closed), 35 (closed), 36 (open), 37 (closed), 38 (closed), 39 (closed), 
    # 40 (closed), 41 (closed), 42 (closed), 43 (closed), 44 (closed), 45 (closed), 
    # 46 (closed), 47 (closed), 48 (closed), 49 (open), 50 (closed)
    assert compute_door_states(50) == ([], [1, 4, 9, 16, 25, 36, 49], "@##@####@######@########@##########@############@#")

def test_hundred_doors():
    # AC-1.1 example: for 100 doors, perfect squares up to 100 remain open: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    assert compute_door_states(100) == ([], [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], 
                                         "@" + "#" * 3 + "@" + "#" * 6 + "@" + "#" * 7 + "@" + "#" * 14 + "@" + "#" * 14 + "@")