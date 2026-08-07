from solution import *

def test_no_pins_knocked_down_scores_zero():
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0  # 0 + 0 + ... = 0

def test_single_roll_knocks_down_pins():
    assert calculate_score([1]) == 1  # 1 pin knocked down

def test_multiple_rolls_no_spares_or_strikes():
    assert calculate_score([1, 2, 3, 4, 5]) == 15  # 1 + 2 + 3 + 4 + 5 = 15

def test_spare_bonus():
    assert calculate_score([5, 5, 3]) == 16  # 5 + 5 + next roll 3 = 16
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # 1 + 2 + 5 + 5 + next roll 3 = 19

def test_strike_bonus():
    assert calculate_score([10, 3, 4]) == 24  # 10 + next two rolls (3 + 4) = 24
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # 1 + 2 + 10 + next two rolls (3 + 4) = 27

def test_perfect_game_scores_300():
    assert calculate_score([10] * 12) == 300  # 12 strikes = 300

def test_combined_spares_and_strikes():
    assert calculate_score([10, 5, 5, 3]) == 36  # strike + spare + next roll = 10 + (5 + 5) + 3 = 36
    assert calculate_score([1, 2, 10, 5, 5, 3]) == 39  # open frame + strike + spare + next roll = 1 + 2 + 10 + (5 + 5) + 3 = 39

def test_tenth_frame_spare():
    assert calculate_score([0] * 18 + [5, 5, 3]) == 13  # spare in the tenth frame = 5 + 5 + next roll 3 = 13