# test_fibonacci.py

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

def test_fibonacci_position_4():
    # The number at position 4 is defined as 2 (1 + 1).
    assert fibonacci(4) == 2

def test_fibonacci_position_5():
    # The number at position 5 is defined as 3 (2 + 1).
    assert fibonacci(5) == 3

def test_fibonacci_position_6():
    # The number at position 6 is defined as 5 (3 + 2).
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    # The refusal carries exactly the message "Fibonacci sequence is not defined for negative numbers".
    import pytest
    with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
        fibonacci(-1)

def test_fibonacci_negative_position_2():
    # A negative position is refused as an invalid value.
    with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
        fibonacci(-10)