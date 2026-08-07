# test_prime_factor_decomposition.py

from solution import prime_factor_decomposition

def test_decomposing_number_1():
    # 1 has no prime factors
    assert prime_factor_decomposition(1) == []

def test_decomposing_prime_number_2():
    # 2 is a prime number, so its only factor is itself
    assert prime_factor_decomposition(2) == [2]

def test_decomposing_prime_number_3():
    # 3 is a prime number, so its only factor is itself
    assert prime_factor_decomposition(3) == [3]

def test_decomposing_composite_number_4():
    # 4 = 2 * 2
    assert prime_factor_decomposition(4) == [2, 2]

def test_decomposing_composite_number_6():
    # 6 = 2 * 3
    assert prime_factor_decomposition(6) == [2, 3]

def test_decomposing_composite_number_8():
    # 8 = 2 * 2 * 2
    assert prime_factor_decomposition(8) == [2, 2, 2]

def test_decomposing_composite_number_9():
    # 9 = 3 * 3
    assert prime_factor_decomposition(9) == [3, 3]

def test_decomposing_large_number():
    # 5^9 * 7^13 = 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7
    assert prime_factor_decomposition(5**9 * 7**13) == [5] * 9 + [7] * 13

def test_decomposing_other_composite_number_10():
    # 10 = 2 * 5
    assert prime_factor_decomposition(10) == [2, 5]