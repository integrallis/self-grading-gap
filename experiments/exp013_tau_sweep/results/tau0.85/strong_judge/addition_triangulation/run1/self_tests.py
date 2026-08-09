# test_two_number_adder.py

from solution import add_two_numbers

def test_add_two_positive_integers():
    # 3 + 5 = 8
    assert add_two_numbers(3, 5) == 8

def test_add_two_other_positive_integers():
    # 4 + 7 = 11
    assert add_two_numbers(4, 7) == 11

def test_add_negative_and_positive_integer():
    # -2 + 5 = 3
    assert add_two_numbers(-2, 5) == 3

def test_add_two_negative_integers():
    # -3 + -7 = -10
    assert add_two_numbers(-3, -7) == -10

def test_add_zero_and_positive_integer():
    # 0 + 5 = 5
    assert add_two_numbers(0, 5) == 5

def test_add_zero_and_negative_integer():
    # 0 + -5 = -5
    assert add_two_numbers(0, -5) == -5

def test_add_two_zeros():
    # 0 + 0 = 0
    assert add_two_numbers(0, 0) == 0

def test_add_large_integers():
    # 1000000 + 2000000 = 3000000
    assert add_two_numbers(1000000, 2000000) == 3000000