from solution import prime_factors

def test_decomposing_number_1():
    # The number 1 has no prime factors
    assert prime_factors(1) == []

def test_decomposing_prime_number_2():
    # The prime number 2 yields itself
    assert prime_factors(2) == [2]

def test_decomposing_prime_number_3():
    # The prime number 3 yields itself
    assert prime_factors(3) == [3]

def test_decomposing_composite_number_4():
    # The composite number 4 yields two 2s (2 * 2 = 4)
    assert prime_factors(4) == [2, 2]

def test_decomposing_composite_number_6():
    # The composite number 6 yields a 2 and a 3 (2 * 3 = 6)
    assert prime_factors(6) == [2, 3]

def test_decomposing_composite_number_8():
    # The composite number 8 yields three 2s (2 * 2 * 2 = 8)
    assert prime_factors(8) == [2, 2, 2]

def test_decomposing_composite_number_9():
    # The composite number 9 yields two 3s (3 * 3 = 9)
    assert prime_factors(9) == [3, 3]

def test_decomposing_large_composite_number():
    # For 5^9 * 7^13, we have:
    # 5^9 = 5, 5, 5, 5, 5, 5, 5, 5, 5 (nine 5s)
    # 7^13 = 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7 (thirteen 7s)
    expected = [5] * 9 + [7] * 13
    assert prime_factors(5**9 * 7**13) == expected