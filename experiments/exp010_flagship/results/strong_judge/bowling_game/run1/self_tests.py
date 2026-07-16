# your complete test file
from solution import *

def test_score_no_pins_knocked_down():
    # No rolls, score should be 0
    assert calculate_score([]) == 0
    # All misses, score should still be 0
    assert calculate_score([0] * 20) == 0

def test_spare_bonus():
    # Spare of 5 and 5 followed by a roll of 3: 5 + 5 + 3 = 13; total = 16
    assert calculate_score([5, 5, 3]) == 16
    # Open frame of 1 and 2, then a spare of 5 and 5 followed by a roll of 3: 1 + 2 + 5 + 5 + 3 = 16; total = 19
    assert calculate_score([1, 2, 5, 5, 3]) == 19

def test_strike_bonus():
    # Strike followed by rolls of 3 and 4: 10 + 3 + 4 = 17; total = 24
    assert calculate_score([10, 3, 4]) == 24
    # Open frame of 1 and 2, then a strike followed by rolls of 3 and 4: 1 + 2 + 10 + 3 + 4 = 20; total = 27
    assert calculate_score([1, 2, 10, 3, 4]) == 27

def test_perfect_game():
    # Perfect game: 12 strikes; total = 300
    assert calculate_score([10]*12) == 300

def test_combined_spares_and_strikes():
    # Combination of strikes and spares: 10 + 3 + 7 + 5 + 5 + 10 + 2 + 3 = 20 + 15 + 20 + 15 + 5 = 75
    assert calculate_score([10, 3, 7, 5, 5, 10, 2, 3]) == 75
    # Another combination: 1 + 9 + 10 + 5 + 5 + 2 = 20 + 12 + 2 = 54
    assert calculate_score([1, 9, 10, 5, 5, 2]) == 54

def test_final_frame_spare():
    # Final frame with a spare of 5 and 5 followed by a roll of 2: 5 + 5 + 2 = 12
    assert calculate_score([0] * 18 + [5, 5, 2]) == 12

def test_final_frame_strike():
    # Final frame with a strike followed by rolls of 3 and 4: 10 + 3 + 4 = 17
    assert calculate_score([0] * 18 + [10, 3, 4]) == 17