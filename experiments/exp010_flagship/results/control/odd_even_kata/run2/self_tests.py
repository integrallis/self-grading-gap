# test_solution.py

from solution import announce_number, announce_range

def test_announce_number_even():
    assert announce_number(2) == "Even"  # Positive even number
    assert announce_number(4) == "Even"  # Positive even number
    assert announce_number(-4) == "-4"   # Negative even number

def test_announce_number_odd_prime():
    assert announce_number(3) == "3"     # Odd prime
    assert announce_number(5) == "5"     # Odd prime
    assert announce_number(11) == "11"    # Odd prime

def test_announce_number_odd():
    assert announce_number(1) == "Odd"    # Positive odd non-prime
    assert announce_number(9) == "Odd"    # Positive odd non-prime
    assert announce_number(25) == "Odd"   # Positive odd non-prime

def test_announce_number_zero():
    assert announce_number(0) == "0"      # Zero

def test_announce_number_negative():
    assert announce_number(-1) == "-1"    # Negative odd
    assert announce_number(-2) == "-2"    # Negative even

def test_announce_range_with_valid_range():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Range from 1 to 10
    assert announce_range(-5, 3) == "Odd Even 3"  # Range from -5 to 3, starts at 1
    assert announce_range(0, 2) == "0 Odd Even"  # Range from 0 to 2

def test_announce_range_with_invalid_range():
    assert announce_range(5, 3) == ""  # Start exceeds end
    assert announce_range(100, 100) == "Even"  # Single even number in range
    assert announce_range(1, 150)  # Long range; the exact output isn't specified but should not be empty