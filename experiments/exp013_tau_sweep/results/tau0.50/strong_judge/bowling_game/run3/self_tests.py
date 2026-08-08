import pytest
from solution import calculate_score

def test_no_pins_knocked_down():
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0  # 0 pins in all rolls

def test_single_roll_knocked_down():
    assert calculate_score([1]) == 1  # 1 pin knocked down

def test_spare_bonus():
    assert calculate_score([5, 5, 3]) == 16  # Spare (5+5) + next roll (3) = 16
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # Open frame (1+2) + Spare (5+5) + next roll (3) = 19
    assert calculate_score([0, 0] * 9 + [5, 5, 7]) == 17  # All misses (0) + Spare (5+5) + bonus (7) = 17

def test_strike_bonus():
    assert calculate_score([10, 3, 4]) == 24  # Strike (10) + next two rolls (3+4) = 24
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # Open frame (1+2) + Strike (10) + next two rolls (3+4) = 27

def test_perfect_game():
    assert calculate_score([10] * 12) == 300  # 12 strikes = 300 points

def test_mixed_game():
    assert calculate_score([10, 3, 4, 5, 5]) == 34  # Strike + (3+4) + Spare (5+5) = 34
    assert calculate_score([10, 10, 10, 3, 4, 0]) == 77  # 3 strikes + (3+4) + next roll (0) = 77

def test_complete_all_miss_game():
    assert calculate_score([0] * 20) == 0  # All misses in a complete game