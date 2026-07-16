# test_solution.py

from solution import fibonacci_lookup

def test_fibonacci_lookup_position_1():
    # The Fibonacci sequence starts with 0, so the number at position 1 is 0.
    assert fibonacci_lookup(1) == 0

def test_fibonacci_lookup_position_2():
    # The second number in the Fibonacci sequence is 1.
    assert fibonacci_lookup(2) == 1

def test_fibonacci_lookup_position_3():
    # The third number in the Fibonacci sequence is also 1.
    assert fibonacci_lookup(3) == 1

def test_fibonacci_lookup_position_10():
    # The Fibonacci sequence up to position 10 is: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34
    # Therefore, the number at position 10 is 34.
    assert fibonacci_lookup(10) == 34

def test_fibonacci_lookup_position_15():
    # The Fibonacci sequence up to position 15 gives us 377.
    assert fibonacci_lookup(15) == 377

def test_fibonacci_lookup_negative_position():
    # A negative position should raise a TypeError.
    with pytest.raises(TypeError):
        fibonacci_lookup(-1)

def test_fibonacci_lookup_position_0():
    # Position 0 should raise a TypeError with the specific message.
    with pytest.raises(TypeError, match="Fibonacci numbers start from 1"):
        fibonacci_lookup(0)