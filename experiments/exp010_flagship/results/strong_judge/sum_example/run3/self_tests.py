# test_solution.py

from solution import add_numbers

def test_add_two_positive_numbers():
    # 1 plus 1 is 2
    assert add_numbers(1, 1) == 2

def test_add_negative_and_positive():
    # -1 plus 1 is 0
    assert add_numbers(-1, 1) == 0

def test_add_two_negative_numbers():
    # -5 plus -3 is -8
    assert add_numbers(-5, -3) == -8

def test_add_zero_to_positive():
    # Adding 0 to 5 results in 5
    assert add_numbers(5, 0) == 5

def test_add_positive_to_zero():
    # Adding 0 to 5 results in 5
    assert add_numbers(0, 5) == 5

def test_add_zero_to_negative():
    # Adding 0 to -3 results in -3
    assert add_numbers(-3, 0) == -3

def test_add_negative_to_zero():
    # Adding 0 to -3 results in -3
    assert add_numbers(0, -3) == -3

def test_add_zero_to_zero():
    # Adding 0 to 0 results in 0
    assert add_numbers(0, 0) == 0