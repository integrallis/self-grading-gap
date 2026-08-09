from solution import calculate_score

def test_no_pins_knocked_down():
    # missed rolls, total score = 0
    assert calculate_score([]) == 0

def test_single_roll_knocks_down_pins():
    # 5 pins down, total score = 5
    assert calculate_score([5]) == 5

def test_multiple_rolls_no_bonuses():
    # 1 + 2 + 3 + 4 = 10
    assert calculate_score([1, 2, 3, 4]) == 10

def test_spare_bonus():
    # 5 + 5 (spare) + 3 (bonus) = 5 + 5 + 3 = 13
    # Total score = 13 + 3 (the bonus roll) = 16
    assert calculate_score([5, 5, 3]) == 16

def test_spare_bonus_after_open_frame():
    # 1 + 2 + 5 + 5 (spare) + 3 (bonus) = 1 + 2 + 5 + 5 + 3 = 16
    assert calculate_score([1, 2, 5, 5, 3]) == 16

def test_strike_bonus():
    # strike (10) + 3 + 4 (bonus) = 10 + 3 + 4 = 17
    # Total score = 17 + 7 (the next frame) = 24
    assert calculate_score([10, 3, 4]) == 24

def test_strike_bonus_after_open_frame():
    # 1 + 2 + strike (10) + 3 + 4 (bonus) = 1 + 2 + 10 + 3 + 4 = 20
    assert calculate_score([1, 2, 10, 3, 4]) == 20

def test_perfect_game():
    # 12 strikes (10 × 12) = 300
    assert calculate_score([10] * 12) == 300

def test_final_frame_spare_bonus():
    # 0 + 0 + ... + 5 + 5 (spare) + 7 (bonus) = 5 + 5 + 7 = 17
    assert calculate_score([0] * 18 + [5, 5, 7]) == 17

def test_completed_all_miss_game():
    # 20 missed rolls, total score = 0
    assert calculate_score([0] * 20) == 0

def test_spare_without_bonus():
    # 5 + 5 (spare) = 10, no bonus roll yet
    assert calculate_score([5, 5]) == 10

def test_strike_with_one_bonus_roll():
    # strike (10) + 3 (bonus) = 13
    assert calculate_score([10, 3]) == 13