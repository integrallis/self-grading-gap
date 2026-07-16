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
    # 1 door -> after 1 walk: 1 is toggled, ends open.
    state_list, open_positions, state_string = compute_door_states(1)
    assert state_list == [True]  # Door 1 is open
    assert open_positions == [1]  # Open door position is 1
    assert state_string == "@"  # "@" for open

def test_two_doors():
    # AC-1.3: Door 2 ends closed: it is toggled twice, by walks 1 and 2.
    # 2 doors -> after 1 walk: 1 toggled; after 2 walks: 1 toggled, 2 toggled.
    state_list, open_positions, state_string = compute_door_states(2)
    assert state_list == [True, False]  # Door 1 is open, Door 2 is closed
    assert open_positions == [1]  # Open door position is 1
    assert state_string == "@#"  # "@" for open, "#" for closed

def test_ten_doors():
    # AC-1.1: For 10 doors, open doors are 1, 4, 9.
    # 1 toggled -> open; 2 toggled -> closed; 3 toggled -> closed; 4 toggled -> open (4 is a perfect square); 
    # 5 toggled -> closed; 6 toggled -> closed; 7 toggled -> closed; 8 toggled -> closed; 9 toggled -> open (9 is a perfect square); 
    # 10 toggled -> closed.
    state_list, open_positions, state_string = compute_door_states(10)
    assert state_list == [True, False, False, True, False, False, False, False, True, False]  # Open doors: 1, 4, 9
    assert open_positions == [1, 4, 9]  # Open positions: 1, 4, 9
    assert state_string == "@##@####@#"  # Corresponding string

def test_one_hundred_doors():
    # AC-1.1: For 100 doors, open doors are perfect squares: 1, 4, 9, 16, 25, 36, 49, 64, 81, 100.
    # After all walks, only perfect squares will be open.
    state_list, open_positions, state_string = compute_door_states(100)
    assert state_list == [i**0.5 % 1 == 0 for i in range(1, 101)]  # Open doors are perfect squares
    assert open_positions == [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]  # Perfect squares
    assert state_string == "@##@####@#@##@#@#@#@#"  # Corresponding string with perfect squares open