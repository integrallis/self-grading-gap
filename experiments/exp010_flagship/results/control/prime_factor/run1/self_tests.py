from solution import prime_factors

def test_decomposing_number_one():
    # The number 1 has no prime factors, so the output should be an empty list.
    assert prime_factors(1) == []

def test_decomposing_prime_number_two():
    # The prime number 2 yields a single factor: itself.
    assert prime_factors(2) == [2]

def test_decomposing_prime_number_three():
    # The prime number 3 yields a single factor: itself.
    assert prime_factors(3) == [3]

def test_decomposing_composite_number_four():
    # The composite number 4 can be expressed as 2 * 2.
    assert prime_factors(4) == [2, 2]

def test_decomposing_composite_number_six():
    # The composite number 6 can be expressed as 2 * 3.
    assert prime_factors(6) == [2, 3]

def test_decomposing_composite_number_eight():
    # The composite number 8 can be expressed as 2 * 2 * 2.
    assert prime_factors(8) == [2, 2, 2]

def test_decomposing_composite_number_nine():
    # The composite number 9 can be expressed as 3 * 3.
    assert prime_factors(9) == [3, 3]

def test_decomposing_large_number():
    # The number 5^9 * 7^13 can be expressed as nine 5s followed by thirteen 7s.
    assert prime_factors(5**9 * 7**13) == [5]*9 + [7]*13