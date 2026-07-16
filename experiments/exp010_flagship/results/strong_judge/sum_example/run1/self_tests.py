from solution import *

def test_add_two_positive_numbers():
    # 1 + 1 = 2
    assert add(1, 1) == 2

def test_add_negative_and_positive_number():
    # -1 + 1 = 0
    assert add(-1, 1) == 0

def test_add_two_negative_numbers():
    # -5 + -3 = -8
    assert add(-5, -3) == -8

def test_add_zero_to_positive_number():
    # 0 + 5 = 5
    assert add(0, 5) == 5

def test_add_positive_number_to_zero():
    # 5 + 0 = 5
    assert add(5, 0) == 5

def test_add_zero_to_negative_number():
    # 0 + -5 = -5
    assert add(0, -5) == -5

def test_add_negative_number_to_zero():
    # -5 + 0 = -5
    assert add(-5, 0) == -5

def test_add_zero_to_zero():
    # 0 + 0 = 0
    assert add(0, 0) == 0

def test_add_two_positive_numbers_general():
    # 2 + 3 = 5
    assert add(2, 3) == 5

def test_add_negative_and_positive_number_general():
    # -2 + 3 = 1
    assert add(-2, 3) == 1

def test_add_two_negative_numbers_general():
    # -2 + -3 = -5
    assert add(-2, -3) == -5