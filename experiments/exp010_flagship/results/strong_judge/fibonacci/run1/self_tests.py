# test_fibonacci.py

import pytest
from solution import fibonacci_lookup

def test_fibonacci_position_1():
    # The number at position 1 is 0.
    assert fibonacci_lookup(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is 1.
    assert fibonacci_lookup(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is 1.
    assert fibonacci_lookup(3) == 1

def test_fibonacci_position_10():
    # The number at position 10 yields 34.
    assert fibonacci_lookup(10) == 34

def test_fibonacci_position_15():
    # The number at position 15 yields 377.
    assert fibonacci_lookup(15) == 377

def test_fibonacci_position_20():
    # The number at position 20 yields 4181.
    assert fibonacci_lookup(20) == 4181

def test_fibonacci_negative_position():
    # A negative position is refused with a type error.
    with pytest.raises(TypeError):
        fibonacci_lookup(-1)

def test_fibonacci_position_0():
    # Position 0 is refused with a type error whose message is exactly "Fibonacci numbers start from 1".
    with pytest.raises(TypeError) as exc_info:
        fibonacci_lookup(0)
    assert str(exc_info.value) == "Fibonacci numbers start from 1"