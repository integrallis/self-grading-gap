import pytest

def test_fibonacci_position_1():
    # The number at position 1 is defined as 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is defined as 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is defined as 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The number at position 6 is defined as 5.
    assert fibonacci(6) == 5

def test_fibonacci_position_10():
    # The number at position 10 is defined as 34.
    assert fibonacci(10) == 34

def test_fibonacci_position_100():
    # The number at position 100 is defined as 218922995834555169026.
    assert fibonacci(100) == 218922995834555169026

def test_fibonacci_negative_position():
    # A negative position should be refused with a specific message.
    with pytest.raises(Exception) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"