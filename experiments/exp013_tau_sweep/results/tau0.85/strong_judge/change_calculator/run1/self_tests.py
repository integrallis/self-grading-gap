# test_coin_change_maker.py

from solution import change_maker

def test_change_maker_single_denomination():
    # Test a single denomination of 25
    assert change_maker(25) == [25]  # 25 yields one 25

def test_change_maker_repeated_denomination():
    # Test an amount that requires repeats of one denomination, e.g., 50
    assert change_maker(50) == [25, 25]  # 50 yields two 25s

def test_change_maker_mixed_amount():
    # Test a mixed amount, e.g., 41
    assert change_maker(41) == [25, 10, 5, 1]  # 41 yields 25, 10, 5, 1 in that order

def test_change_maker_zero_amount():
    # Test zero amount which should yield no coins
    assert change_maker(0) == []  # An amount of zero yields an empty collection of coins

def test_change_maker_non_example_amount():
    # Test a non-example amount, e.g., 37
    assert change_maker(37) == [25, 10, 1, 1]  # 37 - 25 = 12; 12 - 10 = 2; then two 1s