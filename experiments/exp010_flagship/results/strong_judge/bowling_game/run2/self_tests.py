# your complete test file
def test_score_rolls_with_no_bonuses():
    # A roll that knocks down no pins adds nothing; total score should be 0
    assert calculate_bowling_score([]) == 0
    # All missed rolls
    assert calculate_bowling_score([0] * 20) == 0

def test_spare_bonus():
    # A spare of 5 and 5 followed by a 3
    # Frame score = 5 + 5 + next roll (3) = 5 + 5 + 3 = 16
    assert calculate_bowling_score([5, 5, 3]) == 16
    # An open frame of 1 and 2, then a spare of 5 and 5 followed by a 3
    # Frame score = 1 + 2 + 5 + 5 + next roll (3) = 1 + 2 + 5 + 5 + 3 = 19
    assert calculate_bowling_score([1, 2, 5, 5, 3]) == 19
    # A spare in the tenth frame with one bonus roll
    # Frame score = 0 + 0 + 5 + 5 + next roll (7) = 0 + 0 + 5 + 5 + 7 = 17
    assert calculate_bowling_score([0] * 18 + [5, 5, 7]) == 17

def test_strike_bonus():
    # A strike followed by rolls of 3 and 4
    # Frame score = 10 + next two rolls (3 and 4) = 10 + 3 + 4 = 24
    assert calculate_bowling_score([10, 3, 4]) == 24
    # An open frame of 1 and 2, then a strike followed by rolls of 3 and 4
    # Frame score = 1 + 2 + 10 + next two rolls (3 and 4) = 1 + 2 + 10 + 3 + 4 = 27
    assert calculate_bowling_score([1, 2, 10, 3, 4]) == 27

def test_perfect_game():
    # A perfect game of twelve strikes
    # Total score = 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + 10 + two bonus rolls (10 + 10) = 300
    assert calculate_bowling_score([10] * 12) == 300