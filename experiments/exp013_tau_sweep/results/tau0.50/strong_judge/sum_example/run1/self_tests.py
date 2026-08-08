from solution import add_numbers

def test_add_two_positive_numbers():
    # 1 + 1 = 2
    assert add_numbers(1, 1) == 2

def test_add_negative_and_positive_number():
    # -1 + 1 = 0
    assert add_numbers(-1, 1) == 0

def test_add_two_negative_numbers():
    # -5 + -3 = -8
    assert add_numbers(-5, -3) == -8

def test_add_zero_and_positive_number():
    # 0 + 5 = 5
    assert add_numbers(0, 5) == 5

def test_add_positive_number_and_zero():
    # 5 + 0 = 5
    assert add_numbers(5, 0) == 5

def test_add_zero_and_negative_number():
    # 0 + -5 = -5
    assert add_numbers(0, -5) == -5

def test_add_negative_number_and_zero():
    # -5 + 0 = -5
    assert add_numbers(-5, 0) == -5