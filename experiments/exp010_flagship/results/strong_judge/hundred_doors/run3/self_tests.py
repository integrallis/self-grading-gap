import pytest
from solution import compute_door_states

def test_zero_doors():
    # Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_door_states(0) == ([], [], '')

def test_negative_doors():
    # A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    with pytest.raises(Exception) as exc:
        compute_door_states(-1)
    assert str(exc.value) == "door count must be non-negative"

def test_one_door():
    # For 1 door, after 1 walk, it is toggled once and ends open.
    assert compute_door_states(1) == ([True], [1], '@')

def test_two_doors():
    # For 2 doors, door 1 is toggled once (open), door 2 is toggled twice (closed).
    assert compute_door_states(2) == ([True, False], [1], '@#')

def test_ten_doors():
    # For 10 doors, the open doors are 1, 4, 9.
    assert compute_door_states(10) == ([True, False, False, True, False, False, False, False, True, False], 
                                        [1, 4, 9], 
                                        '@##@####@#')

def test_fifty_doors():
    # For 50 doors, the open doors are 1, 4, 9, 16, 25, 36, 49.
    assert compute_door_states(50) == ([True, False, False, True, False, False, False, False, True, False,
                                         False, False, False, True, False, False, False, False, True, False,
                                         False, False, False, True, False, False, False, False, True, False,
                                         False, False, False, True, False, False, False, False, True, False,
                                         False, False, False, True, False], 
                                        [1, 4, 9, 16, 25, 36, 49], 
                                        '@##@####@######@########@##########@############@#')

def test_one_hundred_doors():
    # For 100 doors, the open doors are 1, 4, 9, 16, 25, 36, 49, 64, 81, 100.
    assert compute_door_states(100) == ([True, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False, False, False, False, True, False,
                                          False, False, False, True, False],
                                         [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], 
                                         '@##@####@#@####@#@##@####@#@##@####@#@####@#')

def test_seventeen_doors():
    # For 17 doors, the open doors are 1, 4, 9, 16.
    assert compute_door_states(17) == ([True, False, False, True, False, False, False, False, True, False,
                                         False, False, False, True, False, False, False, False], 
                                        [1, 4, 9, 16], 
                                        '@##@####@######@#')

@pytest.mark.parametrize("door_count, expected_states, expected_positions, expected_string", [
    (3, [True, False, False], [1], '@#@'),
    (26, [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False], [1, 4, 9, 16], '@##@####@#'),
    (99, [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [1, 4, 9, 16, 25, 36, 49, 64, 81], '@##@####@######@########@##########@############@#'),
    (101, [True, False, False, True, False, False, False, False, True, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False], [1, 4, 9, 16, 25, 36, 49, 64, 81, 100], '@##@####@######@########@##########@############@#')
])
def test_parametrized_doors(door_count, expected_states, expected_positions, expected_string):
    assert compute_door_states(door_count) == (expected_states, expected_positions, expected_string)