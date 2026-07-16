# test_fibonacci.py

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

def test_fibonacci_negative_position():
    # Negative position should raise an error
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"