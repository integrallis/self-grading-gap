from solution import fibonacci

def test_fibonacci_position_1():
    # The Fibonacci number at position 1 is defined as 0.
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The Fibonacci number at position 2 is defined as 1.
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The Fibonacci number at position 3 is defined as 1.
    assert fibonacci(3) == 1

def test_fibonacci_position_6():
    # The Fibonacci number at position 6 is defined as the sum of the two before it: 2 + 3 = 5.
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # A negative position should raise a ValueError with a specific message.
    with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
        fibonacci(-1)

def test_fibonacci_zero_position():
    # A position of 0 should also raise a ValueError with the same message.
    with pytest.raises(ValueError, match="Fibonacci sequence is not defined for negative numbers"):
        fibonacci(0)