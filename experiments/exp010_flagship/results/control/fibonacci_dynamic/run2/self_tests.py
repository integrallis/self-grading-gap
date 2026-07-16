# test_fibonacci.py

from solution import fibonacci

def test_fibonacci_position_1():
    # Fibonacci(1) = 0
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # Fibonacci(2) = 1
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # Fibonacci(3) = 1
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # Fibonacci(6) = 5
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # Fibonacci(-1) should raise a ValueError with a specific message
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"