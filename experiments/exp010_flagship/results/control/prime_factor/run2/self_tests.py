from solution import prime_factors

def test_decompose_number_1():
    # 1 has no prime factors
    assert prime_factors(1) == []

def test_decompose_prime_number_2():
    # 2 is a prime number
    assert prime_factors(2) == [2]

def test_decompose_prime_number_3():
    # 3 is a prime number
    assert prime_factors(3) == [3]

def test_decompose_composite_number_4():
    # 4 = 2 * 2
    assert prime_factors(4) == [2, 2]

def test_decompose_composite_number_6():
    # 6 = 2 * 3
    assert prime_factors(6) == [2, 3]

def test_decompose_composite_number_8():
    # 8 = 2 * 2 * 2
    assert prime_factors(8) == [2, 2, 2]

def test_decompose_composite_number_9():
    # 9 = 3 * 3
    assert prime_factors(9) == [3, 3]

def test_decompose_large_number_5_to_9th_power_times_7_to_13th_power():
    # 5^9 * 7^13 = nine 5s followed by thirteen 7s
    assert prime_factors(5**9 * 7**13) == [5] * 9 + [7] * 13