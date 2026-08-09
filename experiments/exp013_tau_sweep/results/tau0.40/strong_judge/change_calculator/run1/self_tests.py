from solution import make_change

def test_make_change_single_denomination():
    # 25 yields one 25
    assert make_change(25) == [25]
    
def test_make_change_repeats_of_one_denomination():
    # 50 yields two 25s
    assert make_change(50) == [25, 25]
    
def test_make_change_mixed_amounts():
    # 41 yields 25, 10, 5, 1 in that order
    assert make_change(41) == [25, 10, 5, 1]

def test_make_change_zero_amount():
    # An amount of zero yields an empty collection of coins
    assert make_change(0) == []