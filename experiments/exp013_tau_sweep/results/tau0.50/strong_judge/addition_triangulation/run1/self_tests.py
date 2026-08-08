# test_add_two_numbers.py

from solution import add_two_numbers

def test_add_two_positive_integers():
    # Adding 3 and 5 yields 8
    assert add_two_numbers(3, 5) == 8

def test_add_two_other_positive_integers():
    # Adding 4 and 7 yields 11
    assert add_two_numbers(4, 7) == 11

def test_add_negative_and_positive_integer():
    # Adding -2 and 5 yields 3
    assert add_two_numbers(-2, 5) == 3

def test_add_two_negative_integers():
    # Adding -3 and -5 yields -8
    assert add_two_numbers(-3, -5) == -8

def test_add_zero_and_positive_integer():
    # Adding 0 and 5 yields 5
    assert add_two_numbers(0, 5) == 5

def test_add_zero_and_negative_integer():
    # Adding 0 and -5 yields -5
    assert add_two_numbers(0, -5) == -5

def test_add_two_large_integers():
    # Adding 1000000 and 2000000 yields 3000000
    assert add_two_numbers(1000000, 2000000) == 3000000

def test_add_two_large_negative_integers():
    # Adding -1000000 and -2000000 yields -3000000
    assert add_two_numbers(-1000000, -2000000) == -3000000