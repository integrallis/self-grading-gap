# test_solution.py
from solution import announce_number, announce_range

def test_announce_number_positive_even():
    assert announce_number(2) == "Even"  # Even number

def test_announce_number_odd_prime():
    assert announce_number(3) == "3"  # Odd prime

def test_announce_number_positive_odd_non_prime():
    assert announce_number(1) == "Odd"  # Positive odd non-prime

def test_announce_number_zero():
    assert announce_number(0) == "0"  # Zero

def test_announce_number_negative_even():
    assert announce_number(-4) == "-4"  # Negative even number

def test_announce_number_negative_odd():
    assert announce_number(-3) == "-3"  # Negative odd number

def test_announce_range_from_1_to_10():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Range 1-10

def test_announce_range_negative_to_positive():
    assert announce_range(-5, 3) == "Odd Even 3"  # Range -5 to 3

def test_announce_range_zero_to_two():
    assert announce_range(0, 2) == "0 Odd Even"  # Range 0-2

def test_announce_range_start_exceeds_end():
    assert announce_range(5, 3) == ""  # Start exceeds end

def test_announce_range_large_span():
    assert announce_range(1, 100)  # Should produce a result, but exact output not specified
    assert announce_range(5, 150)  # Should produce a result, but exact output not specified