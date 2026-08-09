# test_solution.py

from solution import announce_number, announce_range

def test_announce_number_even():
    assert announce_number(2) == "Even"  # Positive even number

def test_announce_number_odd_prime():
    assert announce_number(3) == "3"  # Odd prime number

def test_announce_number_positive_odd_not_prime():
    assert announce_number(1) == "Odd"  # Positive odd number that is not prime

def test_announce_number_zero():
    assert announce_number(0) == "0"  # Zero

def test_announce_number_negative_even():
    assert announce_number(-4) == "-4"  # Negative even number

def test_announce_number_negative_odd():
    assert announce_number(-3) == "-3"  # Negative odd number

def test_announce_range_positive_numbers():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Range from 1 to 10

def test_announce_range_negative_start():
    assert announce_range(-5, 3) == "Odd Even 3"  # Range from -5 to 3, starting at 1

def test_announce_range_zero_start():
    assert announce_range(0, 2) == "0 Odd Even"  # Range from 0 to 2

def test_announce_range_start_exceeds_end():
    assert announce_range(5, 3) == ""  # Start exceeds end

def test_announce_range_large_span():
    assert announce_range(1, 100)  # No specific expected value, just ensuring it runs
    assert announce_range(5, 150)  # No specific expected value, just ensuring it runs