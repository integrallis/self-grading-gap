# test_fibonacci.py

from solution import fibonacci

def test_fibonacci_position_1():
    # Position 1 yields 0 (base case)
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # Position 2 yields 1 (base case)
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # Position 3 yields 1 (1 + 0)
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # Position 6 yields 5 (2 + 3)
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # Negative position is refused
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"