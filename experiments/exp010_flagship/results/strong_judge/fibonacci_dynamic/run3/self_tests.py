# test_fibonacci.py

import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # The number at position 1 is 0
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is 1
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is 1
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The number at position 6 is 5
    assert fibonacci(6) == 5

def test_fibonacci_position_10():
    # The number at position 10 is 34
    assert fibonacci(10) == 34

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"