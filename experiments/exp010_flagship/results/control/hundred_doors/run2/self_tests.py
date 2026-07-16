# test_solution.py

from solution import compute_door_states

def test_zero_doors():
    # AC-3.1: Zero doors yield an empty state list, an empty list of open positions, and an empty string.
    assert compute_door_states(0) == ([], [], "")

def test_negative_doors():
    # AC-3.2: A negative door count is rejected as an error with exactly the message "door count must be non-negative".
    with pytest.raises(ValueError, match="door count must be non-negative"):
        compute_door_states(-1)

def test_one_door():
    # AC-1.2: A single door ends open: the only walk toggles it once.
    # 1 door, after 1 walk: door 1 is toggled once (open)
    open_doors = compute_door_states(1)[1]
    assert open_doors == [1]

def test_two_doors():
    # AC-1.3: Door 2 ends closed: it is toggled twice, by walks 1 and 2.
    # 2 doors, after 2 walks: door 1 is toggled (open), door 2 is toggled twice (closed)
    open_doors = compute_door_states(2)[1]
    assert open_doors == [1]

def test_ten_doors():
    # AC-1.1: For 10 doors, the perfect squares are 1, 4, 9.
    # 10 doors, after 10 walks: doors 1, 4, 9 are toggled (open)
    open_doors = compute_door_states(10)[1]
    assert open_doors == [1, 4, 9]

def test_one_hundred_doors():
    # AC-1.1: For 100 doors, the perfect squares are 1, 4, 9, 16, 25, 36, 49, 64, 81, 100.
    # 100 doors, after 100 walks: doors at perfect square positions remain open
    open_doors = compute_door_states(100)[1]
    expected_open_doors = [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
    assert open_doors == expected_open_doors

def test_open_closed_indicators_for_ten_doors():
    # AC-2.1: Check final state as open/closed indicators for 10 doors.
    # 10 doors status: [open, closed, closed, open, closed, closed, closed, closed, open, closed]
    indicators = compute_door_states(10)[0]
    expected_indicators = ["@", "#", "#", "@", "#", "#", "#", "#", "@", "#"]
    assert indicators == expected_indicators

def test_string_representation_for_ten_doors():
    # AC-2.3: Check string representation for 10 doors.
    # 10 doors status: "@##@####@#"
    state_string = compute_door_states(10)[2]
    assert state_string == "@##@####@#"

def test_open_positions_for_ten_doors():
    # AC-2.2: Check final positions of open doors for 10 doors.
    # Open doors are at positions [1, 4, 9].
    open_positions = compute_door_states(10)[1]
    assert open_positions == [1, 4, 9]

def test_open_closed_indicators_for_one_hundred_doors():
    # AC-2.1: Check final state as open/closed indicators for 100 doors.
    indicators = compute_door_states(100)[0]
    expected_indicators = ["@", "#"] * 50
    expected_indicators[0] = "@"
    expected_indicators[3] = "@"
    expected_indicators[8] = "@"
    expected_indicators[15] = "@"
    expected_indicators[24] = "@"
    expected_indicators[35] = "@"
    expected_indicators[48] = "@"
    expected_indicators[63] = "@"
    expected_indicators[80] = "@"
    expected_indicators[99] = "@"
    assert indicators == expected_indicators

def test_string_representation_for_one_hundred_doors():
    # AC-2.3: Check string representation for 100 doors.
    state_string = compute_door_states(100)[2]
    expected_string = "@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#@#"
    assert state_string == expected_string