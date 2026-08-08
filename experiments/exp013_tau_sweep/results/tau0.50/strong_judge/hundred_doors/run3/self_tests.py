import pytest
from solution import compute_final_door_states

def test_zero_doors():
    # AC-3.1: Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_final_door_states(0) == ([], [], "")

def test_negative_doors():
    # AC-3.2: A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    with pytest.raises(Exception, match=r"\Adoor count must be non-negative\Z"):
        compute_final_door_states(-1)

def test_one_door():
    # AC-1.2: A single door ends open: the only walk toggles it once.
    # 1 door: Walk 1 toggles door 1 -> door 1 is open
    final_state = compute_final_door_states(1)
    assert final_state[0] == [True]  # Open/closed indicator
    assert final_state[1] == [1]      # Open door positions
    assert final_state[2] == "@"       # String representation

def test_two_doors():
    # AC-1.3: Door 2 ends closed: it is toggled twice, by walks 1 and 2.
    # 2 doors: Walk 1 toggles door 1, Walk 2 toggles door 2 -> door 1 is open, door 2 is closed
    final_state = compute_final_door_states(2)
    assert final_state[0] == [True, False]  # Open/closed indicators
    assert final_state[1] == [1]             # Open door positions
    assert final_state[2] == "@#"             # String representation

def test_fifty_doors():
    # AC-1.1: For 50 doors, perfect squares are 1, 4, 9, 16, 25, 36, 49
    final_state = compute_final_door_states(50)
    expected_open_positions = [1, 4, 9, 16, 25, 36, 49]
    assert final_state[0] == [i in expected_open_positions for i in range(1, 51)]  # Open/closed indicators
    assert final_state[1] == expected_open_positions  # Open door positions
    assert final_state[2] == "@##@####@#\n#####@####\n####@#####\n#####@####\n########@#"  # String representation

def test_ten_doors():
    # AC-1.1: For 10 doors, after all walks, doors at perfect-square positions remain open (1, 4, 9)
    # Perfect squares up to 10 are 1, 4, and 9
    final_state = compute_final_door_states(10)
    assert final_state[0] == [True, False, False, True, False, False, False, False, True, False]  # Open/closed indicators
    assert final_state[1] == [1, 4, 9]  # Open door positions
    assert final_state[2] == "@##@####@#"  # String representation

def test_one_hundred_doors():
    # AC-1.1: For 100 doors, perfect squares are 1, 4, 9, 16, 25, 36, 49, 64, 81, 100
    final_state = compute_final_door_states(100)
    expected_open_positions = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    assert final_state[0] == [i in expected_open_positions for i in range(1, 101)]  # Open/closed indicators
    assert final_state[1] == expected_open_positions  # Open door positions
    assert final_state[2] == "@##@####@#\n#####@####\n####@#####\n#####@####\n########@#\n#########@\n###@######\n##########\n@#########\n#########@"  # String representation