# test_coin_change_maker.py

from solution import make_change

def test_single_denomination_25():
    # 25 yields one 25
    assert make_change(25) == [25]

def test_repeated_denomination_50():
    # 50 yields two 25s
    assert make_change(50) == [25, 25]

def test_mixed_amount_41():
    # 41 yields 25, 10, 5, 1 in that order
    assert make_change(41) == [25, 10, 5, 1]

def test_zero_amount():
    # An amount of zero yields an empty collection of coins
    assert make_change(0) == []

def test_non_example_amount_30():
    # 30 yields one 25 and one 5
    assert make_change(30) == [25, 5]