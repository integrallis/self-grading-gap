from solution import prime_factor_decomposition

def test_decompose_number_1():
    # The number 1 has no prime factors.
    assert prime_factor_decomposition(1) == []

def test_decompose_prime_number_2():
    # The prime number 2 yields a single factor: itself.
    assert prime_factor_decomposition(2) == [2]

def test_decompose_prime_number_3():
    # The prime number 3 yields a single factor: itself.
    assert prime_factor_decomposition(3) == [3]

def test_decompose_composite_number_4():
    # The number 4 is 2 * 2.
    assert prime_factor_decomposition(4) == [2, 2]

def test_decompose_composite_number_6():
    # The number 6 is 2 * 3.
    assert prime_factor_decomposition(6) == [2, 3]

def test_decompose_composite_number_8():
    # The number 8 is 2 * 2 * 2.
    assert prime_factor_decomposition(8) == [2, 2, 2]

def test_decompose_composite_number_9():
    # The number 9 is 3 * 3.
    assert prime_factor_decomposition(9) == [3, 3]

def test_decompose_large_number():
    # The number 5^9 * 7^13 yields nine 5s followed by thirteen 7s.
    assert prime_factor_decomposition(5**9 * 7**13) == [5] * 9 + [7] * 13