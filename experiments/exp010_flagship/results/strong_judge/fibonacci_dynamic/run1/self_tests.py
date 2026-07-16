# test_fibonacci.py

import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # The Fibonacci number at position 1 is 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The Fibonacci number at position 2 is 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The Fibonacci number at position 3 is 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_4():
    # The Fibonacci number at position 4 is 2.
    assert fibonacci(4) == 2

def test_fibonacci_position_5():
    # The Fibonacci number at position 5 is 3.
    assert fibonacci(5) == 3

def test_fibonacci_position_6():
    # The Fibonacci number at position 6 is 5.
    assert fibonacci(6) == 5

def test_fibonacci_position_101():
    # The Fibonacci number at position 101 is 354224848179261915075.
    assert fibonacci(101) == 354224848179261915075

def test_fibonacci_negative_position():
    # A negative position is refused.
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"

def test_fibonacci_memoization():
    # Verify that Fibonacci numbers are computed efficiently for large positions.
    assert fibonacci(100) == 354224848179261915075  # First call to compute and cache
    assert fibonacci(100) == 354224848179261915075  # Second call should use cached value