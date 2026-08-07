# test_fibonacci.py

import pytest
from solution import fibonacci_lookup

def test_fibonacci_position_1():
    # The Fibonacci number at position 1 is 0
    assert fibonacci_lookup(1) == 0

def test_fibonacci_position_2():
    # The Fibonacci number at position 2 is 1
    assert fibonacci_lookup(2) == 1

def test_fibonacci_position_3():
    # The Fibonacci number at position 3 is 1
    assert fibonacci_lookup(3) == 1

def test_fibonacci_position_10():
    # The Fibonacci number at position 10 is 34
    assert fibonacci_lookup(10) == 34

def test_fibonacci_position_15():
    # The Fibonacci number at position 15 is 377
    assert fibonacci_lookup(15) == 377

def test_fibonacci_position_11():
    # The Fibonacci number at position 11 is 55
    assert fibonacci_lookup(11) == 55

def test_fibonacci_negative_position():
    # A negative position should raise a TypeError
    with pytest.raises(TypeError) as exc:
        fibonacci_lookup(-1)
    assert str(exc.value) == "Fibonacci numbers start from 1"

def test_fibonacci_position_0():
    # Position 0 should raise a TypeError with a specific message
    with pytest.raises(TypeError) as exc:
        fibonacci_lookup(0)
    assert str(exc.value) == "Fibonacci numbers start from 1"