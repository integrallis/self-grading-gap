# test_solution.py

from solution import compute_final_door_states

def test_zero_doors():
    # AC-3.1: Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_final_door_states(0) == ([], [], "")

def test_negative_doors():
    # AC-3.2: A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    import pytest
    with pytest.raises(Exception) as excinfo:
        compute_final_door_states(-1)
    assert str(excinfo.value) == "door count must be non-negative"

def test_one_door():
    # AC-1.2: For 1 door, it is toggled once and ends open.
    # Final state: [True] -> open-door positions: [1] -> string: "@" 
    assert compute_final_door_states(1) == ([True], [1], "@")

def test_two_doors():
    # AC-1.3: For 2 doors, door 2 is toggled twice and ends closed.
    # Final state: [True, False] -> open-door positions: [1] -> string: "@#"
    assert compute_final_door_states(2) == ([True, False], [1], "@#")

def test_three_doors():
    # Walk 1 toggles all doors: [True, True, True]
    # Walk 2 toggles door 2: [True, False, True]
    # Walk 3 toggles door 3: [True, False, False]
    # Final state: [True, False, False] -> open-door positions: [1] -> string: "@##"
    assert compute_final_door_states(3) == ([True, False, False], [1], "@##")

def test_ten_doors():
    # Walks 1 to 10 toggle doors at perfect-square positions: 1, 4, 9 are open.
    # Final state: [True, False, False, True, False, False, False, False, True, False] 
    # -> open-door positions: [1, 4, 9] -> string: "@##@####@#"
    assert compute_final_door_states(10) == ([True, False, False, True, False, False, False, False, True, False], [1, 4, 9], "@##@####@#")

def test_fifty_doors():
    # For 50 doors, open doors are at perfect-square positions: 1, 4, 9, 16, 25, 36, 49
    # Final state: [True, False, False, True, False, False, False, False, True, False, 
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False,
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False]
    # -> open-door positions: [1, 4, 9, 16, 25, 36, 49] 
    # -> string: "@##@####@#@##@##@##@##@#"
    assert compute_final_door_states(50) == (
        [True, False, False, True, False, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False],
        [1, 4, 9, 16, 25, 36, 49],
        "@##@####@#@##@##@##@##@#"
    )

def test_one_hundred_doors():
    # For 100 doors, open doors are at perfect-square positions: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    # Final state: [True, False, False, True, False, False, False, False, True, False, 
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False,
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False,
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False,
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False,
    #               False, False, True, False, False, False, True, False, False, False,
    #               True, False, False, False, True, False, False, False, True, False]
    # -> open-door positions: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100] 
    # -> string: "@##@####@#@##@##@##@##@#"
    assert compute_final_door_states(100) == (
        [True, False, False, True, False, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False,
         False, False, True, False, False, False, True, False, False, False,
         True, False, False, False, True, False, False, False, True, False],
        [1, 4, 9, 16, 25, 36, 49, 64, 81, 100],
        "@##@####@#@##@##@##@##@#"
    )