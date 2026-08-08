# test_solution.py

from solution import add_numbers

def test_add_positive_numbers():
    # 1 plus 1 is 2
    assert add_numbers(1, 1) == 2

def test_add_negative_and_positive_number():
    # -1 plus 1 is 0
    assert add_numbers(-1, 1) == 0

def test_add_two_negative_numbers():
    # -5 plus -3 is -8
    assert add_numbers(-5, -3) == -8

def test_add_zero_to_positive_number():
    # 0 plus 5 is 5
    assert add_numbers(0, 5) == 5

def test_add_positive_number_to_zero():
    # 5 plus 0 is 5
    assert add_numbers(5, 0) == 5

def test_add_zero_to_negative_number():
    # 0 plus -5 is -5
    assert add_numbers(0, -5) == -5

def test_add_negative_number_to_zero():
    # -5 plus 0 is -5
    assert add_numbers(-5, 0) == -5

def test_add_zero_to_zero():
    # 0 plus 0 is 0
    assert add_numbers(0, 0) == 0

def test_add_two_positive_numbers():
    # 2 plus 3 is 5
    assert add_numbers(2, 3) == 5

def test_add_negative_and_positive_number_general():
    # -7 plus 4 is -3
    assert add_numbers(-7, 4) == -3