from solution import make_change

def test_make_change_single_denomination():
    # 25 = [25]
    assert make_change(25) == [25]

def test_make_change_repeated_denomination():
    # 50 = [25, 25]
    assert make_change(50) == [25, 25]

def test_make_change_mixed_amount():
    # 41 = [25, 10, 5, 1]
    assert make_change(41) == [25, 10, 5, 1]

def test_make_change_zero_amount():
    # 0 = []
    assert make_change(0) == []

def test_make_change_non_example_amount():
    # 33 = [25, 5, 1, 1]
    assert make_change(33) == [25, 5, 1, 1]