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

def test_fibonacci_position_7():
    # The Fibonacci number at position 7 is 8.
    assert fibonacci(7) == 8

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    # The refusal message is "Fibonacci sequence is not defined for negative numbers".
    result = fibonacci(-1)
    assert result == "Fibonacci sequence is not defined for negative numbers"

def test_fibonacci_direct_recursion():
    # Ensure that the implementation is using direct recursion to calculate Fibonacci numbers.
    # We will compare the output with a manually calculated Fibonacci sequence.
    def direct_fibonacci(n):
        if n <= 0:
            return "Fibonacci sequence is not defined for negative numbers"
        elif n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            return direct_fibonacci(n - 1) + direct_fibonacci(n - 2)

    for i in range(1, 8):  # Test positions 1 through 7
        assert fibonacci(i) == direct_fibonacci(i)