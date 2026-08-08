from solution import announce_number, announce_range

def test_announce_number_positive_even():
    # 2 is a positive even number
    assert announce_number(2) == "Even"

def test_announce_number_odd_prime():
    # 3 is an odd prime number
    assert announce_number(3) == "3"
    # 5 is an odd prime number
    assert announce_number(5) == "5"
    # 11 is an odd prime number
    assert announce_number(11) == "11"

def test_announce_number_positive_odd_not_prime():
    # 1 is a positive odd number that is not prime
    assert announce_number(1) == "Odd"
    # 9 is a positive odd number that is not prime
    assert announce_number(9) == "Odd"
    # 25 is a positive odd number that is not prime
    assert announce_number(25) == "Odd"

def test_announce_number_zero():
    # 0 is announced as "0"
    assert announce_number(0) == "0"

def test_announce_number_negative_even():
    # -4 is a negative number, announced as itself
    assert announce_number(-4) == "-4"

def test_announce_number_negative_odd():
    # -3 is a negative number, announced as itself
    assert announce_number(-3) == "-3"

def test_announce_range_positive_range():
    # range from 1 to 10: Odd Even 3 Even 5 Even 7 Even Odd Even
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"

def test_announce_range_negative_start():
    # range from -5 to 3 starts at 1: Odd Even 3
    assert announce_range(-5, 3) == "Odd Even 3"

def test_announce_range_start_zero():
    # range from 0 to 2: 0 Odd Even
    assert announce_range(0, 2) == "0 Odd Even"

def test_announce_range_start_exceeds_end():
    # start exceeds end: empty string
    assert announce_range(5, 3) == ""

def test_announce_range_large_span():
    # range from 1 to 100: should produce a non-empty result
    result = announce_range(1, 100)
    assert result != ""

def test_announce_range_another_large_span():
    # range from 5 to 150: should produce a non-empty result
    result = announce_range(5, 150)
    assert result != ""