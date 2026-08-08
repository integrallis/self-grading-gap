import pytest
from solution import fibonacci_number_at_position

def test_fibonacci_number_at_position_1():
    # Position 1: Fibonacci(1) = 0
    assert fibonacci_number_at_position(1) == 0

def test_fibonacci_number_at_position_2():
    # Position 2: Fibonacci(2) = 1
    assert fibonacci_number_at_position(2) == 1

def test_fibonacci_number_at_position_3():
    # Position 3: Fibonacci(3) = 1
    assert fibonacci_number_at_position(3) == 1

def test_fibonacci_number_at_position_4():
    # Position 4: Fibonacci(4) = 2
    assert fibonacci_number_at_position(4) == 2

def test_fibonacci_number_at_position_10():
    # Position 10: Fibonacci(10) = 34
    assert fibonacci_number_at_position(10) == 34

def test_fibonacci_number_at_position_15():
    # Position 15: Fibonacci(15) = 377
    assert fibonacci_number_at_position(15) == 377

def test_fibonacci_number_at_position_negative():
    # Negative position: should raise TypeError
    with pytest.raises(TypeError):
        fibonacci_number_at_position(-1)

def test_fibonacci_number_at_position_0():
    # Position 0: should raise TypeError with specific message
    with pytest.raises(TypeError, match=r"\AFibonacci numbers start from 1\Z"):
        fibonacci_number_at_position(0)