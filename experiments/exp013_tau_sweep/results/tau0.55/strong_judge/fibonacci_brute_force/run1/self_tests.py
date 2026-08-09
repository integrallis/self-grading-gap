# test_fibonacci.py

import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # The number at position 1 is 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The number at position 6 is 5.
    assert fibonacci(6) == 5

def test_fibonacci_position_7():
    # The number at position 7 is 8. (F(6) + F(5) = 5 + 3 = 8)
    assert fibonacci(7) == 8

def test_fibonacci_position_8():
    # The number at position 8 is 13. (F(7) + F(6) = 8 + 5 = 13)
    assert fibonacci(8) == 13

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    with pytest.raises(ValueError, match="^Fibonacci sequence is not defined for negative numbers$"):
        fibonacci(-1)