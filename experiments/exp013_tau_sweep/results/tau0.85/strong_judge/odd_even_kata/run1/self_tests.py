from solution import announce_number, announce_range

def test_announce_single_positive_even():
    assert announce_number(2) == "Even"  # Positive even number

def test_announce_single_positive_odd_prime():
    assert announce_number(3) == "3"  # Odd prime number

def test_announce_single_positive_odd_non_prime():
    assert announce_number(1) == "Odd"  # Positive odd non-prime

def test_announce_single_zero():
    assert announce_number(0) == "0"  # Zero

def test_announce_single_negative_even():
    assert announce_number(-4) == "-4"  # Negative even number

def test_announce_single_negative_odd():
    assert announce_number(-5) == "-5"  # Negative odd number

def test_announce_range_positive():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Range from 1 to 10

def test_announce_range_negative_start():
    assert announce_range(-5, 3) == "Odd Even 3"  # Range from -5 to 3, starts at 1

def test_announce_range_zero_start():
    assert announce_range(0, 2) == "0 Odd Even"  # Range from 0 to 2

def test_announce_range_start_exceeds_end():
    assert announce_range(5, 3) == ""  # Start exceeds end, should return empty string

def test_announce_range_large_span():
    assert announce_range(1, 100) == "Odd Even 3 Even 5 Even 7 Even Odd Even 11 Even 13 Odd Even 17 Odd Even 19 Odd Even 21 Odd Even 23 Odd Even 25 Odd Even 27 Odd Even 29 Odd Even 31 Odd Even 33 Odd Even 35 Odd Even 37 Odd Even 39 Odd Even 41 Odd Even 43 Odd Even 45 Odd Even 47 Odd Even 49 Odd Even 51 Odd Even 53 Odd Even 55 Odd Even 57 Odd Even 59 Odd Even 61 Odd Even 63 Odd Even 65 Odd Even 67 Odd Even 69 Odd Even 71 Odd Even 73 Odd Even 75 Odd Even 77 Odd Even 79 Odd Even 81 Odd Even 83 Odd Even 85 Odd Even 87 Odd Even 89 Odd Even 91 Odd Even 93 Odd Even 95 Odd Even 97 Odd Even 99 Even"  # Full range announcement for 1 to 100

    assert announce_range(5, 150) == "5 Even 7 Even Odd Even 11 Even 13 Odd Even 17 Odd Even 19 Odd Even 21 Odd Even 23 Odd Even 25 Odd Even 27 Odd Even 29 Odd Even 31 Odd Even 33 Odd Even 35 Odd Even 37 Odd Even 39 Odd Even 41 Odd Even 43 Odd Even 45 Odd Even 47 Odd Even 49 Odd Even 51 Odd Even 53 Odd Even 55 Odd Even 57 Odd Even 59 Odd Even 61 Odd Even 63 Odd Even 65 Odd Even 67 Odd Even 69 Odd Even 71 Odd Even 73 Odd Even 75 Odd Even 77 Odd Even 79 Odd Even 81 Odd Even 83 Odd Even 85 Odd Even 87 Odd Even 89 Odd Even 91 Odd Even 93 Odd Even 95 Odd Even 97 Odd Even 99 Odd Even 101 Odd Even 103 Odd Even 105 Odd Even 107 Odd Even 109 Odd Even 111 Odd Even 113 Odd Even 115 Odd Even 117 Odd Even 119 Odd Even 121 Odd Even 123 Odd Even 125 Odd Even 127 Odd Even 129 Odd Even 131 Odd Even 133 Odd Even 135 Odd Even 137 Odd Even 139 Odd Even 141 Odd Even 143 Odd Even 145 Odd Even 147 Odd Even 149 Odd"  # Full range announcement for 5 to 150