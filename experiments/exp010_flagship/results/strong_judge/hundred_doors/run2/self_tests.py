# test_solution.py

from solution import compute_door_states

def test_zero_doors():
    # Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_door_states(0) == ([], [], "")

def test_negative_doors():
    # A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    import pytest
    with pytest.raises(Exception) as excinfo:
        compute_door_states(-1)
    assert str(excinfo.value) == "door count must be non-negative"

def test_one_door():
    # For 1 door, it will be toggled once, so it ends open.
    # Final state: [True], open positions: [1], string: "@".
    assert compute_door_states(1) == ([True], [1], "@")

def test_two_doors():
    # For 2 doors, door 1 will end open, door 2 will end closed.
    # Final state: [True, False], open positions: [1], string: "@#".
    assert compute_door_states(2) == ([True, False], [1], "@#")

def test_three_doors():
    # For 3 doors, door 1 will end open, door 2 will end closed, door 3 will end closed.
    # Final state: [True, False, False], open positions: [1], string: "@##".
    assert compute_door_states(3) == ([True, False, False], [1], "@##")

def test_ten_doors():
    # For 10 doors, doors at positions 1, 4, and 9 will end open.
    # Final state: [True, False, False, True, False, False, False, False, True, False], open positions: [1, 4, 9], string: "@##@####@#".
    assert compute_door_states(10) == ([True, False, False, True, False, False, False, False, True, False], [1, 4, 9], "@##@####@#")

def test_one_hundred_doors():
    # For 100 doors, doors at positions 1, 4, 9, 16, 25, 36, 49, 64, 81, and 100 will end open.
    # Final state: [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False]
    # open positions: [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], string: "@##@####@#...@"
    expected_state = [i*i <= 100 for i in range(1, 11)] + [False]*90  # 10 squares <= 100
    expected_positions = [i*i for i in range(1, 11)]
    expected_string = "@" + "#"*2 + "@" + "#"*5 + "@" + "#"*8 + "@" + "#"*11 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@" + "#"*10 + "@"
    assert compute_door_states(100) == (expected_state, expected_positions, expected_string)

def test_fifty_doors():
    # For 50 doors, doors at positions 1, 4, 9, 16, 25, 36, 49 will end open.
    # Final state: [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], open positions: [1, 4, 9, 16, 25, 36, 49], string: "@##@####@######@########@#".
    expected_state = [i*i <= 50 for i in range(1, 8)] + [False]*43  # 7 squares <= 50
    expected_positions = [i*i for i in range(1, 8)]
    expected_string = "@" + "#"*2 + "@" + "#"*5 + "@" + "#"*8 + "@" + "#"*10 + "@"  # example for 50 doors
    expected_string += "#"*43  # Total length of 50
    assert compute_door_states(50) == (expected_state, expected_positions, expected_string)

def test_twenty_six_doors():
    # For 26 doors, doors at positions 1, 4, 9, 16, 25 will end open.
    # Final state: [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False], open positions: [1, 4, 9, 16, 25], string: "@##@####@######@#".
    expected_state = [i*i <= 26 for i in range(1, 7)] + [False]*20  # 5 squares <= 26
    expected_positions = [i*i for i in range(1, 7)]
    expected_string = "@" + "#"*2 + "@" + "#"*5 + "@" + "#"*8 + "@" + "#"*10 + "#"  # example for 26 doors
    expected_string += "#"*21  # Total length of 26
    assert compute_door_states(26) == (expected_state, expected_positions, expected_string)