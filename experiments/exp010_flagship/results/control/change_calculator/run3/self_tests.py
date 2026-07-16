from solution import make_change

def test_single_denomination_25():
    # 25 yields one 25
    assert make_change(25) == [25]

def test_single_denomination_50():
    # 50 yields two 25s
    assert make_change(50) == [25, 25]

def test_single_denomination_10():
    # 10 yields one 10
    assert make_change(10) == [10]

def test_single_denomination_5():
    # 5 yields one 5
    assert make_change(5) == [5]

def test_single_denomination_1():
    # 1 yields one 1
    assert make_change(1) == [1]

def test_mixed_amount_41():
    # 41 yields 25, 10, 5, 1 in that order
    assert make_change(41) == [25, 10, 5, 1]

def test_mixed_amount_99():
    # 99 yields 25, 25, 25, 10, 10, 5, 1, 1, 1, 1 in that order
    assert make_change(99) == [25, 25, 25, 10, 10, 5, 1, 1, 1, 1]

def test_no_change_due():
    # 0 yields an empty collection of coins
    assert make_change(0) == []