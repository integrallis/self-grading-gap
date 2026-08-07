from solution import announce_single, announce_range

def test_announcing_positive_even_number():
    # 2 is a positive even number, should be announced as "Even"
    assert announce_single(2) == "Even"

def test_announcing_odd_prime_number():
    # 3 is an odd prime, should be announced as "3"
    assert announce_single(3) == "3"

def test_announcing_positive_odd_non_prime_number():
    # 9 is a positive odd number that is not prime, should be announced as "Odd"
    assert announce_single(9) == "Odd"

def test_announcing_zero():
    # 0 should be announced as "0"
    assert announce_single(0) == "0"

def test_announcing_negative_even_number():
    # -4 is a negative even number, should be announced as "-4"
    assert announce_single(-4) == "-4"

def test_announcing_negative_odd_number():
    # -3 is a negative odd number, should be announced as "-3"
    assert announce_single(-3) == "-3"

def test_announcing_range_positive_numbers():
    # Range from 1 to 10: 1=Odd, 2=Even, 3=3, 4=Even, 5=5, 6=Even, 7=7, 8=Even, 9=Odd, 10=Even
    assert announce_range(1, 10) == "Odd Even 3 Even 5 Even 7 Even Odd Even"

def test_announcing_range_with_negative_start():
    # Range from -5 to 3: starts at 1 due to specification, announces 1=Odd, 2=Even, 3=3
    assert announce_range(-5, 3) == "Odd Even 3"

def test_announcing_range_with_zero_start():
    # Range from 0 to 2: 0=0, 1=Odd, 2=Even
    assert announce_range(0, 2) == "0 Odd Even"

def test_announcing_range_with_start_exceeding_end():
    # Range from 5 to 3: start exceeds end, should be an empty string
    assert announce_range(5, 3) == ""

def test_announcing_large_range():
    # Range from 1 to 100: testing a long range
    # The expected output includes "Odd" for all odd composites and their own value for odd primes
    expected_output = "Odd Even 3 Even Odd Even 5 Even Odd Even 7 Even 9 Even 11 Even Odd Even 13 Even Odd Even 15 Even Odd Even 17 Even Odd Even 19 Even Odd Even 21 Even Odd Even 23 Even Odd Even 25 Even Odd Even 27 Even Odd Even 29 Even Odd Even 31 Even Odd Even 33 Even Odd Even 35 Even Odd Even 37 Even Odd Even 39 Even Odd Even 41 Even Odd Even 43 Even Odd Even 45 Even Odd Even 47 Even Odd Even 49 Even Odd Even 51 Even Odd Even 53 Even Odd Even 55 Even Odd Even 57 Even Odd Even 59 Even Odd Even 61 Even Odd Even 63 Even Odd Even 65 Even Odd Even 67 Even Odd Even 69 Even Odd Even 71 Even Odd Even 73 Even Odd Even 75 Even Odd Even 77 Even Odd Even 79 Even Odd Even 81 Even Odd Even 83 Even Odd Even 85 Even Odd Even 87 Even Odd Even 89 Even Odd Even 91 Even Odd Even 93 Even Odd Even 95 Even Odd Even 97 Even Odd Even 99 Even"
    assert announce_range(1, 100) == expected_output

def test_announcing_large_negative_range():
    # Range from -150 to -100: start raised to 1, end is -100, hence start exceeds end, should be an empty string
    assert announce_range(-150, -100) == ""