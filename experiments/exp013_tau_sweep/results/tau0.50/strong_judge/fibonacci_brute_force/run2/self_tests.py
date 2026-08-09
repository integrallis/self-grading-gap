# test_fibonacci.py

import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # The number at position 1 is defined as 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is defined as 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is defined as 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The number at position 6 follows the recursive definition: 
    # fibonacci(6) = fibonacci(5) + fibonacci(4) 
    # where fibonacci(5) = 3 and fibonacci(4) = 2, thus 3 + 2 = 5.
    assert fibonacci(6) == 5

def test_fibonacci_position_7():
    # The number at position 7 follows the recursive definition: 
    # fibonacci(7) = fibonacci(6) + fibonacci(5) 
    # where fibonacci(6) = 5 and fibonacci(5) = 3, thus 5 + 3 = 8.
    assert fibonacci(7) == 8

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    # The refusal carries the message: "Fibonacci sequence is not defined for negative numbers".
    with pytest.raises(Exception, match=r"\AFibonacci sequence is not defined for negative numbers\Z"):
        fibonacci(-1)

def test_fibonacci_negative_position_2():
    # Another negative position to ensure the same behavior.
    with pytest.raises(Exception, match=r"\AFibonacci sequence is not defined for negative numbers\Z"):
        fibonacci(-10)