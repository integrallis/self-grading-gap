from solution import fibonacci

def test_fibonacci_position_1():
    # The number at position 1 is 0 (F(1) = 0)
    assert fibonacci(1) == 0

def test_fibonacci_position_2():
    # The number at position 2 is 1 (F(2) = 1)
    assert fibonacci(2) == 1

def test_fibonacci_position_3():
    # The number at position 3 is 1 (F(3) = 1)
    assert fibonacci(3) == 1

def test_fibonacci_position_4():
    # The number at position 4 is 2 (F(4) = F(3) + F(2) = 1 + 1 = 2)
    assert fibonacci(4) == 2

def test_fibonacci_position_5():
    # The number at position 5 is 3 (F(5) = F(4) + F(3) = 2 + 1 = 3)
    assert fibonacci(5) == 3

def test_fibonacci_position_6():
    # The number at position 6 is 5 (F(6) = F(5) + F(4) = 3 + 2 = 5)
    assert fibonacci(6) == 5

def test_fibonacci_negative_position():
    # A negative position is refused as an invalid value
    with pytest.raises(ValueError) as excinfo:
        fibonacci(-1)
    assert str(excinfo.value) == "Fibonacci sequence is not defined for negative numbers"