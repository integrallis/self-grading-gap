from solution import prime_factors

def test_prime_factors_of_one():
    # The number 1 has no prime factors.
    assert prime_factors(1) == []

def test_prime_factors_of_two():
    # The prime number 2 yields 2.
    assert prime_factors(2) == [2]

def test_prime_factors_of_three():
    # The prime number 3 yields 3.
    assert prime_factors(3) == [3]

def test_prime_factors_of_four():
    # The composite number 4 yields two 2s, since 4 = 2 * 2.
    assert prime_factors(4) == [2, 2]

def test_prime_factors_of_six():
    # The composite number 6 yields two factors: 2 and 3, since 6 = 2 * 3.
    assert prime_factors(6) == [2, 3]

def test_prime_factors_of_eight():
    # The composite number 8 yields three 2s, since 8 = 2 * 2 * 2.
    assert prime_factors(8) == [2, 2, 2]

def test_prime_factors_of_nine():
    # The composite number 9 yields two 3s, since 9 = 3 * 3.
    assert prime_factors(9) == [3, 3]

def test_prime_factors_of_large_number():
    # The composite number 5^9 * 7^13 yields nine 5s followed by thirteen 7s.
    # 5^9 is 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 (9 times)
    # 7^13 is 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 (13 times)
    assert prime_factors(5**9 * 7**13) == [5] * 9 + [7] * 13