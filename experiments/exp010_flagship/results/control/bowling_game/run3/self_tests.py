from solution import score_bowling_game

def test_no_pins_knocked_down():
    assert score_bowling_game([]) == 0  # No rolls, score is 0

def test_missed_rolls():
    assert score_bowling_game([0, 0, 0, 0]) == 0  # All rolls miss, score is 0

def test_spare_bonus():
    assert score_bowling_game([5, 5, 3]) == 16  # 5 + 5 + next roll (3) = 16
    assert score_bowling_game([1, 2, 5, 5, 3]) == 19  # 1 + 2 + 5 + 5 + next roll (3) = 19

def test_strike_bonus():
    assert score_bowling_game([10, 3, 4]) == 24  # 10 + next two rolls (3 + 4) = 24
    assert score_bowling_game([1, 2, 10, 3, 4]) == 27  # 1 + 2 + 10 + next two rolls (3 + 4) = 27

def test_perfect_game():
    assert score_bowling_game([10] * 12) == 300  # 12 strikes, score is 300