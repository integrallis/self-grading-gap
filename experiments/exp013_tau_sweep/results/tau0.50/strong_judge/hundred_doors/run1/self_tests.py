# test_solution.py

import pytest
from solution import compute_door_states

def test_zero_doors_yields_empty_state():
    # 0 doors yield an empty state list
    assert compute_door_states(0) == ([], [], "")

def test_negative_doors_raises_error():
    # A negative door count is rejected as an error
    with pytest.raises(Exception) as excinfo:
        compute_door_states(-1)
    assert str(excinfo.value) == "door count must be non-negative"

def test_one_door_final_state():
    # 1 door, after 1 walk, door 1 is toggled open
    assert compute_door_states(1) == ([False], [1], "@")

def test_two_doors_final_state():
    # 2 doors, door 1 toggled open, door 2 toggled closed
    assert compute_door_states(2) == ([False, True], [1], "@#")

def test_three_doors_final_state():
    # 3 doors, door 1 toggled open, door 2 toggled closed, door 3 toggled closed
    assert compute_door_states(3) == ([False, True, True], [1], "@##")

def test_four_doors_final_state():
    # 4 doors, doors 1 and 4 are toggled open
    assert compute_door_states(4) == ([False, True, True, False], [1, 4], "@##@")

def test_ten_doors_final_state():
    # 10 doors, doors 1, 4, 9 are toggled open
    assert compute_door_states(10) == ([False, True, True, False, True, False, False, False, True, False], 
                                        [1, 4, 9], "@##@####@#")

def test_fifty_doors_final_state():
    # 50 doors, doors 1, 4, 9, 16, 25, 36, 49 are toggled open (1 to 49)
    assert compute_door_states(50) == ([False, True, True, False, True, False, False, False, True, False,
                                         True, True, True, True, False, True, True, True, True, True,
                                         False, True, True, True, True, True, True, False, True, False,
                                         True, True, True, True, True, False, True, True, True, True,
                                         True, True, True, True, True, True, True, True, True, True],
                                        [1, 4, 9, 16, 25, 36, 49],
                                        "@##@####@######@########@#")

def test_hundred_doors_final_state():
    # 100 doors, doors 1, 4, 9, 16, 25, 36, 49, 64, 81, 100 are toggled open
    assert compute_door_states(100) == ([False, True, True, False, True, False, False, False, True, False,
                                          True, True, True, True, False, True, True, True, True, True,
                                          False, True, True, True, True, True, True, False, True, False,
                                          True, True, True, True, True, False, True, True, True, True,
                                          True, True, True, True, True, True, True, True, True, True,
                                          True, True, False, True, True, True, True, True, True, True,
                                          True, True, True, True, True, True, True, True, True, True,
                                          True, True, False, True, True, True, True, True, True, True,
                                          True, False, True, True, True, False, True],
                                         [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
                                         "@##@####@#@####@######@#@##@##########@#"))

def test_twenty_six_doors_final_state():
    # 26 doors, doors 1, 4, 9, 16, 25 are toggled open
    assert compute_door_states(26) == ([False, True, True, False, True, False, False, False, True, False,
                                         True, True, True, True, False, True, True, True, True, True,
                                         False, True, True, True, True, True, True, False],
                                        [1, 4, 9, 16, 25],
                                        "@##@####@######@#")