from solution import prime_factors

def test_decomposing_number_one():
    # The number 1 has no prime factors.
    assert prime_factors(1) == []

def test_decomposing_prime_two():
    # The prime number 2 yields a single factor: itself.
    assert prime_factors(2) == [2]

def test_decomposing_prime_three():
    # The prime number 3 yields a single factor: itself.
    assert prime_factors(3) == [3]

def test_decomposing_composite_four():
    # The composite number 4 yields its prime factors: 2 and 2.
    assert prime_factors(4) == [2, 2]

def test_decomposing_composite_six():
    # The composite number 6 yields its prime factors: 2 and 3.
    assert prime_factors(6) == [2, 3]

def test_decomposing_composite_eight():
    # The composite number 8 yields its prime factors: 2, 2, and 2.
    assert prime_factors(8) == [2, 2, 2]

def test_decomposing_composite_nine():
    # The composite number 9 yields its prime factors: 3 and 3.
    assert prime_factors(9) == [3, 3]

def test_decomposing_large_composite():
    # The number 5^9 * 7^13 yields nine 5s followed by thirteen 7s.
    # 5^9 = 5, 5, 5, 5, 5, 5, 5, 5, 5
    # 7^13 = 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
    assert prime_factors(5**9 * 7**13) == [5] * 9 + [7] * 13