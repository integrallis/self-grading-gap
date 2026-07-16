from solution import calculate_score

def test_no_pins_knocked_down():
    assert calculate_score([]) == 0  # No rolls, score is 0
    assert calculate_score([0, 0]) == 0  # 0 + 0 = 0
    assert calculate_score([0] * 20) == 0  # 0 for all rolls

def test_spare_bonus():
    assert calculate_score([5, 5, 3]) == 16  # spare (5 + 5) + next roll (3) = 10 + 3 = 13
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # open frame (1 + 2) + spare (5 + 5) + next roll (3) = 3 + 10 + 3 = 16
    assert calculate_score([5, 5, 0]) == 10  # spare (5 + 5) + next roll (0) = 10 + 0 = 10
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 3]) == 16  # 0 frames + spare (5 + 5) + next roll (3) = 0 + 10 + 3 = 13

def test_strike_bonus():
    assert calculate_score([10, 3, 4]) == 24  # strike (10) + next two rolls (3 + 4) = 10 + 7 = 17
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # open frame (1 + 2) + strike (10) + next two rolls (3 + 4) = 3 + 10 + 7 = 20
    assert calculate_score([10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10]) == 300  # 12 strikes = 300
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 4]) == 24  # 0 frames + strike (10) + next two rolls (3 + 4) = 0 + 10 + 7 = 17

def test_mixed_frames():
    assert calculate_score([10, 3, 6, 4, 5, 5]) == 42  # strike (10 + 3 + 6) + (4 + 5 + next roll 5) = 19 + 9 + 15 = 43
    assert calculate_score([1, 4, 10, 2, 3]) == 25  # open frame (1 + 4) + strike (10) + (2 + 3) = 5 + 10 + 5 = 20

def test_tenth_frame_spare():
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 3]) == 16  # 0 frames + spare (5 + 5) + next roll (3) = 0 + 10 + 3 = 13

def test_tenth_frame_strike():
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 10, 3, 4]) == 24  # 0 frames + strike (10) + next two rolls (3 + 4) = 0 + 10 + 7 = 17

def test_perfect_game():
    assert calculate_score([10] * 12) == 300  # 12 strikes = 300