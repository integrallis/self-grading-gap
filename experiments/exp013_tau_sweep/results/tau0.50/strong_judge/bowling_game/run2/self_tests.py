from solution import calculate_score

def test_score_no_rolls():
    # No rolls, score is 0
    assert calculate_score([]) == 0

def test_score_missed_rolls():
    # All rolls miss, score is 0
    assert calculate_score([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]) == 0

def test_score_open_frames():
    # Open frames of 1 and 2, then another open frame of 3 and 4, total = 1 + 2 + 3 + 4 = 10
    assert calculate_score([1, 2, 3, 4]) == 10

def test_score_spare():
    # Spare of 5 and 5 followed by a 3, total = 5 + 5 + 3 = 16
    assert calculate_score([5, 5, 3]) == 16

def test_score_spare_after_open_frame():
    # Open frame of 1 and 2, then a spare of 5 and 5 followed by a 3, total = 1 + 2 + (5 + 5 + 3) = 19
    assert calculate_score([1, 2, 5, 5, 3]) == 19

def test_score_strike():
    # Strike followed by 3 and 4, total = (10 + 3 + 4) + 0 = 24
    assert calculate_score([10, 3, 4]) == 24

def test_score_strike_after_open_frame():
    # Open frame of 1 and 2, then a strike followed by 3 and 4, total = 1 + 2 + (10 + 3 + 4) = 27
    assert calculate_score([1, 2, 10, 3, 4]) == 27

def test_score_perfect_game():
    # Twelve consecutive strikes, total = 10 * 12 = 300
    assert calculate_score([10] * 12) == 300

def test_score_strike_and_spare():
    # Strike followed by a spare, total = (10 + 5 + 5) + 3 = 36
    assert calculate_score([10, 5, 5, 3]) == 36

def test_score_multiple_strikes():
    # Two strikes followed by a 3, total = (10 + 10 + 3) + 0 = 39
    assert calculate_score([10, 10, 3]) == 39

def test_score_spare_then_strike():
    # Spare followed by a strike, total = (5 + 5 + 10) + 3 = 36
    assert calculate_score([5, 5, 10, 3]) == 36

def test_score_tenth_frame_spare():
    # No pins knocked down for the first 18 rolls, then a spare in the 10th frame followed by a 7, total = 5 + 5 + 7 = 17
    assert calculate_score([0] * 18 + [5, 5, 7]) == 17

def test_score_tenth_frame_strike():
    # No pins knocked down for the first 18 rolls, then a strike in the 10th frame followed by 3 and 4, total = 10 + 3 + 4 = 17
    assert calculate_score([0] * 18 + [10, 3, 4]) == 17