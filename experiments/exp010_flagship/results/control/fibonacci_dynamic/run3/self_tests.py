# test_fibonacci.py

from solution import fibonacci

def test_fibonacci_position_1():
    # Expected: 0 (the first number in the Fibonacci sequence)
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # Expected: 1 (the second number in the Fibonacci sequence)
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # Expected: 1 (the third number in the Fibonacci sequence)
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # Expected: 5 (the sixth number in the Fibonacci sequence)
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # Expected: raise ValueError with specific message
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"