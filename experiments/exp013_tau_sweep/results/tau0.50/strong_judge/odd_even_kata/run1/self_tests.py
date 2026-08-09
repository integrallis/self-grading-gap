from solution import announce_number, announce_range

# Test for single number announcements
def test_positive_even_number():
    assert announce_number(2) == "Even"  # Positive even number

def test_odd_prime_number():
    assert announce_number(3) == "3"  # Odd prime number

def test_positive_odd_non_prime_number():
    assert announce_number(1) == "Odd"  # Positive odd non-prime number

def test_zero():
    assert announce_number(0) == "0"  # Zero

def test_negative_even_number():
    assert announce_number(-4) == "-4"  # Negative even number

def test_negative_odd_number():
    assert announce_number(-3) == "-3"  # Negative odd number


# Test for range announcements
def test_range_positive_numbers():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Range from 1 to 10

def test_range_negative_start():
    assert announce_range(-5, 3) == "Odd Even 3"  # Range from -5 to 3 (starts at 1)

def test_range_zero_start():
    assert announce_range(0, 2) == "0 Odd Even"  # Range from 0 to 2

def test_range_start_exceeds_end():
    assert announce_range(5, 3) == ""  # Start exceeds end, should return an empty string

def test_range_large_span():
    assert announce_range(1, 100) == "Odd Even 3 Even 5 Even 7 Even Odd Even Even 11 Even Odd Even Even 13 Even Odd Even Even 17 Even Odd Even Even 19 Even Even 21 Even Odd Even 23 Even Odd Even Even 27 Even Even 29 Even Odd Even Even 31 Even Odd Even Even 35 Even Even 37 Even Odd Even Even 39 Even Even 41 Even Odd Even Even 43 Even Odd Even Even 47 Even Odd Even Even 49 Even Even 51 Even Odd Even Even 53 Even Odd Even Even 57 Even Even 59 Even Odd Even Even 61 Even Odd Even Even 65 Even Even 67 Even Odd Even Even 69 Even Even 71 Even Odd Even Even 73 Even Odd Even Even 77 Even Even 79 Even Odd Even Even 81 Even Even 83 Even Odd Even Even 87 Even Odd Even Even 89 Even Odd Even Even 93 Even Odd Even Even 95 Even Even 97 Even Odd Even Even 99 Even"  # Correct announcements for range from 1 to 100

    assert announce_range(5, 150) == "5 Even 7 Even Odd Even 11 Even Odd Even 13 Even Odd Even 17 Even Odd Even 19 Even Even 21 Even Odd Even 23 Even Odd Even Even 27 Even Even 29 Even Odd Even Even 31 Even Odd Even Even 35 Even Even 37 Even Odd Even Even 39 Even Even 41 Even Odd Even Even 43 Even Odd Even Even 47 Even Odd Even Even 49 Even Even 51 Even Odd Even Even 53 Even Odd Even Even 57 Even Even 59 Even Odd Even Even 61 Even Odd Even Even 65 Even Even 67 Even Odd Even Even 69 Even Even 71 Even Odd Even Even 73 Even Odd Even Even 77 Even Even 79 Even Odd Even Even 81 Even Even 83 Even Odd Even Even 87 Even Odd Even Even 89 Even Odd Even Even 93 Even Odd Even Even 95 Even Even 97 Even Odd Even Even 99 Even Even 101 Even Even 103 Even Odd Even Even 107 Even Even 109 Even Odd Even Even 113 Even Even 115 Even Odd Even Even 117 Even Even 119 Even Odd Even Even 123 Even Even 125 Even Odd Even Even 127 Even Odd Even Even 131 Even Odd Even Even 133 Even Even 135 Even Odd Even Even 137 Even Odd Even Even 141 Even Even 143 Even Odd Even Even 145 Even Odd Even Even 149 Even Odd"  # Correct announcements for range from 5 to 150