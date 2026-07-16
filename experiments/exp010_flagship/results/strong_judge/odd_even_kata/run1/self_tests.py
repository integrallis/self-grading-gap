from solution import announce_single, announce_range

def test_positive_even_number():
    assert announce_single(2) == "Even"  # 2 is a positive even number

def test_odd_prime_number():
    assert announce_single(3) == "3"  # 3 is an odd prime number

def test_positive_odd_not_prime():
    assert announce_single(1) == "Odd"  # 1 is a positive odd number that is not prime

def test_zero():
    assert announce_single(0) == "0"  # 0 is announced as "0"

def test_negative_even_number():
    assert announce_single(-4) == "-4"  # -4 is a negative even number

def test_range_positive_numbers():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Announcements for 1 through 10

def test_range_negative_start():
    assert announce_range(-5, 3) == "Odd Even 3"  # Range starts at 1 for negative start

def test_range_zero_start():
    assert announce_range(0, 2) == "0 Odd Even"  # Range from 0 to 2

def test_range_start_exceeds_end():
    assert announce_range(5, 3) == ""  # Start exceeds end, result is empty string

def test_range_large_span():
    assert announce_range(1, 100)  # Should produce a valid output for a large range

def test_range_large_span_from_5_to_150():
    assert announce_range(5, 150)  # Should produce a valid output for a large range