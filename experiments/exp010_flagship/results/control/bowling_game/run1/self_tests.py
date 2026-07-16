from solution import calculate_score

def test_score_no_pins_knocked_down():
    assert calculate_score([0, 0, 0, 0]) == 0  # Total = 0

def test_score_all_missed_rolls():
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0  # Total = 0

def test_score_spare_bonus():
    assert calculate_score([5, 5, 3]) == 16  # Spare = 5 + 5 + Next roll = 3 -> Total = 5 + 5 + 3 = 16

def test_score_spare_after_open_frame():
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # Open frame = 1 + 2 + Spare = 5 + 5 + Next roll = 3 -> Total = 1 + 2 + 5 + 5 + 3 = 19

def test_score_strike_bonus():
    assert calculate_score([10, 3, 4]) == 24  # Strike = 10 + Next two rolls = 3 + 4 -> Total = 10 + 3 + 4 = 24

def test_score_strike_after_open_frame():
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # Open frame = 1 + 2 + Strike = 10 + Next two rolls = 3 + 4 -> Total = 1 + 2 + 10 + 3 + 4 = 27

def test_score_perfect_game():
    assert calculate_score([10] * 12) == 300  # Perfect game = 12 strikes -> Total = 300