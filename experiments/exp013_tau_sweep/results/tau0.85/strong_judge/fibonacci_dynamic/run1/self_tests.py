# test_fibonacci.py

import pytest
from solution import fibonacci

def test_fibonacci_position_1():
    # Position 1 corresponds to the first number in the Fibonacci sequence, which is 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # Position 2 corresponds to the second number in the Fibonacci sequence, which is 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # Position 3 corresponds to the third number in the Fibonacci sequence, which is 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # Position 6 corresponds to the sixth number in the Fibonacci sequence, which is 5.
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    # The refusal carries the message "Fibonacci sequence is not defined for negative numbers".
    with pytest.raises(Exception) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"

def test_fibonacci_performance():
    # Verify performance by checking a large position (e.g., position 30).
    # The 30th Fibonacci number is 514229 (conventional F(29) when position 1 = 0).
    assert fibonacci(30) == 514229

def test_fibonacci_large_position():
    # Verify a substantially larger position (e.g., position 50).
    # The 50th Fibonacci number is 12586269025 (conventional F(49) when position 1 = 0).
    assert fibonacci(50) == 12586269025