import pytest
from solution import fibonacci_lookup

def test_fibonacci_lookup_position_1():
    # The Fibonacci sequence starts: 0, 1, 1, 2, ...
    assert fibonacci_lookup(1) == 0  # Position 1 is 0

def test_fibonacci_lookup_position_2():
    # The Fibonacci sequence starts: 0, 1, 1, 2, ...
    assert fibonacci_lookup(2) == 1  # Position 2 is 1

def test_fibonacci_lookup_position_3():
    # The Fibonacci sequence starts: 0, 1, 1, 2, ...
    assert fibonacci_lookup(3) == 1  # Position 3 is 1

def test_fibonacci_lookup_position_10():
    # The Fibonacci sequence starts: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...
    assert fibonacci_lookup(10) == 34  # Position 10 is 34

def test_fibonacci_lookup_position_15():
    # The Fibonacci sequence starts: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, ...
    assert fibonacci_lookup(15) == 377  # Position 15 is 377

def test_fibonacci_lookup_negative_position():
    with pytest.raises(TypeError):
        fibonacci_lookup(-1)  # Negative position should raise TypeError

def test_fibonacci_lookup_position_0():
    with pytest.raises(TypeError) as exc_info:
        fibonacci_lookup(0)  # Position 0 should raise TypeError with specific message
    assert str(exc_info.value) == "Fibonacci numbers start from 1"  # Exact error message