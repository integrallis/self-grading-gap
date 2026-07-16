from solution import score_game

def test_score_no_rolls():
    assert score_game([]) == 0  # No rolls, score is 0

def test_score_missed_rolls():
    assert score_game([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0  # All misses, score is 0

def test_score_open_frames():
    assert score_game([1, 2, 3, 4, 5, 6, 7, 8, 9, 0]) == 45  # Open frames, score is 1+2 + 3+4 + 5+6 + 7+8 + 9+0 = 45

def test_score_spare():
    assert score_game([5, 5, 3]) == 13  # Spare of 5+5 adds next roll 3 -> 5+5+3 = 13
    assert score_game([1, 2, 5, 5, 3]) == 16  # Open frame 1+2 + spare 5+5 + next roll 3 -> 1+2+5+5+3 = 16

def test_score_strike():
    assert score_game([10, 3, 4]) == 24  # Strike adds next two rolls 3+4 -> 10+3+4 = 24
    assert score_game([1, 2, 10, 3, 4]) == 27  # Open frame 1+2 + strike + next two rolls 3+4 -> 1+2+10+3+4 = 27

def test_perfect_game():
    assert score_game([10]*12) == 300  # Perfect game, 12 strikes -> score is 300