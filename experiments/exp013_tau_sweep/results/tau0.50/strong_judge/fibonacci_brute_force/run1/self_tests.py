import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # Fibonacci(1) = 0
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # Fibonacci(2) = 1
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # Fibonacci(3) = 1
    assert fibonacci(3) == 1

def test_fibonacci_position_4():
    # Fibonacci(4) = Fibonacci(3) + Fibonacci(2) = 1 + 1 = 2
    assert fibonacci(4) == 2

def test_fibonacci_position_5():
    # Fibonacci(5) = Fibonacci(4) + Fibonacci(3) = 2 + 1 = 3
    assert fibonacci(5) == 3

def test_fibonacci_position_6():
    # Fibonacci(6) = Fibonacci(5) + Fibonacci(4) = 3 + 2 = 5
    assert fibonacci(6) == 5

def test_fibonacci_position_7():
    # Fibonacci(7) = Fibonacci(6) + Fibonacci(5) = 5 + 3 = 8
    assert fibonacci(7) == 8

def test_fibonacci_position_8():
    # Fibonacci(8) = Fibonacci(7) + Fibonacci(6) = 8 + 5 = 13
    assert fibonacci(8) == 13

def test_fibonacci_negative_position():
    # Position -1 is invalid, should raise ValueError with specific message
    with pytest.raises(ValueError, match=r"^Fibonacci sequence is not defined for negative numbers$"):
        fibonacci(-1)