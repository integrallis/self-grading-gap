# test_fibonacci.py

from solution import fibonacci

def test_fibonacci_position_1():
    # The Fibonacci number at position 1 is 0 (0 is the first number in the sequence).
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The Fibonacci number at position 2 is 1 (1 is the second number in the sequence).
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The Fibonacci number at position 3 is 1 (1 is the third number in the sequence).
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The Fibonacci number at position 6 is 5 (the sequence is 0, 1, 1, 2, 3, 5).
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value.
    # The refusal message is "Fibonacci sequence is not defined for negative numbers".
    with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
        fibonacci(-1)