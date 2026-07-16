import pytest
from solution import fibonacci_lookup

def test_fibonacci_position_1():
    # The Fibonacci sequence starts with 0, so position 1 should return 0.
    assert fibonacci_lookup(1) == 0

def test_fibonacci_position_2():
    # The second number in the Fibonacci sequence is 1.
    assert fibonacci_lookup(2) == 1

def test_fibonacci_position_3():
    # The third number in the Fibonacci sequence is also 1.
    assert fibonacci_lookup(3) == 1

def test_fibonacci_position_10():
    # To find the 10th number: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    assert fibonacci_lookup(10) == 34

def test_fibonacci_position_15():
    # To find the 15th number: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377
    assert fibonacci_lookup(15) == 377

def test_fibonacci_negative_position():
    # A negative position should raise a TypeError.
    with pytest.raises(TypeError):
        fibonacci_lookup(-1)

def test_fibonacci_position_0():
    # Position 0 should raise a TypeError with a specific message.
    with pytest.raises(TypeError, match="Fibonacci numbers start from 1"):
        fibonacci_lookup(0)