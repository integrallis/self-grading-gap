from solution import announce_number, announce_range

def test_announce_number_positive_even():
    assert announce_number(2) == "Even"  # positive even number

def test_announce_number_odd_prime():
    assert announce_number(3) == "3"  # odd prime number

def test_announce_number_positive_odd_not_prime():
    assert announce_number(1) == "Odd"  # positive odd number, not prime

def test_announce_number_zero():
    assert announce_number(0) == "0"  # zero

def test_announce_number_negative_even():
    assert announce_number(-4) == "-4"  # negative even number

def test_announce_range_positive_numbers():
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"  # range 1 to 10

def test_announce_range_negative_start():
    assert announce_range(-5, 3) == "Odd Even 3"  # range -5 to 3

def test_announce_range_zero_start():
    assert announce_range(0, 2) == "0 Odd Even"  # range 0 to 2

def test_announce_range_start_exceeds_end():
    assert announce_range(3, 2) == ""  # range 3 to 2

def test_announce_range_long_span():
    assert announce_range(1, 100)  # range 1 to 100 should produce a result
    assert announce_range(5, 150)  # range 5 to 150 should produce a result