# your complete test file
def test_no_pins_knocked_down():
    assert calculate_score([0, 0, 0]) == 0  # 0 + 0 + 0 = 0

def test_all_misses():
    assert calculate_score([0] * 20) == 0  # 20 misses = 0

def test_spare_bonus():
    assert calculate_score([5, 5, 3]) == 16  # (5 + 5 + 3) = 16
    assert calculate_score([1, 2, 5, 5, 3]) == 19  # (1 + 2 + 5 + 5 + 3) = 19

def test_strike_bonus():
    assert calculate_score([10, 3, 4]) == 24  # (10 + 3 + 4) = 24
    assert calculate_score([1, 2, 10, 3, 4]) == 27  # (1 + 2 + 10 + 3 + 4) = 27

def test_perfect_game():
    assert calculate_score([10] * 12) == 300  # 12 strikes = 300