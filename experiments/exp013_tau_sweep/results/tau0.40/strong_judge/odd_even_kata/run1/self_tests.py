from solution import announce_number, announce_range

def test_announce_number_positive_even():
    assert announce_number(2) == "Even"  # Positive even number
    assert announce_number(4) == "Even"  # Positive even number
    assert announce_number(6) == "Even"  # Positive even number

def test_announce_number_odd_prime():
    assert announce_number(3) == "3"  # Odd prime number
    assert announce_number(5) == "5"  # Odd prime number
    assert announce_number(11) == "11"  # Odd prime number

def test_announce_number_positive_odd_non_prime():
    assert announce_number(1) == "Odd"  # Positive odd non-prime
    assert announce_number(9) == "Odd"  # Positive odd non-prime
    assert announce_number(25) == "Odd"  # Positive odd non-prime

def test_announce_number_zero():
    assert announce_number(0) == "0"  # Zero case

def test_announce_number_negative():
    assert announce_number(-1) == "-1"  # Negative odd number
    assert announce_number(-4) == "-4"  # Negative even number
    assert announce_number(-10) == "-10"  # Negative even number

def test_announce_range():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # Normal range
    assert announce_range(-5, 3) == "Odd Even 3"  # Negative start
    assert announce_range(0, 2) == "0 Odd Even"  # Zero start
    assert announce_range(5, 5) == "Odd"  # Single number range
    assert announce_range(10, 1) == ""  # Start exceeds end
    assert announce_range(1, 100)  # Long range
    assert announce_range(5, 150)  # Long range