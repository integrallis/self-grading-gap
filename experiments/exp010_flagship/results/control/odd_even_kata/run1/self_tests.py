# test_solution.py

from solution import announce_number, announce_range

def test_announce_positive_even_number():
    # 2 is a positive even number
    assert announce_number(2) == "Even"

def test_announce_odd_prime_number():
    # 3 is an odd prime
    assert announce_number(3) == "3"

def test_announce_positive_odd_non_prime():
    # 9 is a positive odd number that is not prime
    assert announce_number(9) == "Odd"

def test_announce_zero():
    # 0 is announced as "0"
    assert announce_number(0) == "0"

def test_announce_negative_even_number():
    # -4 is a negative number and is announced as itself
    assert announce_number(-4) == "-4"

def test_announce_negative_odd_number():
    # -3 is a negative number and is announced as itself
    assert announce_number(-3) == "-3"

def test_announce_single_positive_odd_number():
    # 25 is a positive odd number that is not prime
    assert announce_number(25) == "Odd"

def test_announce_range_positive_numbers():
    # Range from 1 to 10: 1 (Odd), 2 (Even), 3 (3), 4 (Even), 5 (5), 6 (Even), 7 (7), 8 (Even), 9 (Odd), 10 (Even)
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"

def test_announce_range_with_negative_start():
    # Range from -5 to 3: starts from 1 (Odd), 2 (Even), 3 (3)
    assert announce_range(-5, 3) == "Odd Even 3"

def test_announce_range_with_zero_start():
    # Range from 0 to 2: 0 (0), 1 (Odd), 2 (Even)
    assert announce_range(0, 2) == "0 Odd Even"

def test_announce_range_with_start_exceeding_end():
    # An empty range where start is greater than end
    assert announce_range(5, 3) == ""

def test_announce_large_range():
    # Large range from 1 to 100: many numbers, but still valid
    assert announce_range(1, 100)  # no specific string to match; checking for no errors

def test_announce_large_range_start_zero():
    # Large range from 0 to 150: 0 (0), then continue upwards
    assert announce_range(0, 150)  # no specific string to match; checking for no errors