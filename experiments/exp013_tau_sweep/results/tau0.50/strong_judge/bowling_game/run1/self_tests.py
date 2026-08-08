from solution import calculate_score

def test_rolls_with_no_bonuses():
    # No pins knocked down, the score is 0.
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0  # 0

def test_spare_bonus():
    # Spare of 5 and 5 followed by a roll of 3
    assert calculate_score([5, 5, 3]) == 16  # 5 + 5 + 3 = 13 + 3 (spare bonus) = 16

    # Open frame of 1 and 2, then a spare of 5 and 5 followed by a roll of 3
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # 1 + 2 + 5 + 5 + 3 = 16 + 3 (spare bonus) = 19

def test_strike_bonus():
    # A strike followed by 3 and 4
    assert calculate_score([10, 3, 4]) == 24  # 10 + 3 + 4 = 17 + 7 (strike bonus) = 24

    # Open frame of 1 and 2, then a strike followed by 3 and 4
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # 1 + 2 + 10 + 3 + 4 = 20 + 7 (strike bonus) = 27

def test_perfect_game():
    # Twelve consecutive strikes (10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10)
    assert calculate_score([10] * 12) == 300  # 300 for perfect game