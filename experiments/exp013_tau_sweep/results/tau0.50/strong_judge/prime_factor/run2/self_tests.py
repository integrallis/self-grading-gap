from solution import prime_factor_decomposition

def test_decompose_number_one():
    # The number 1 has no prime factors
    assert prime_factor_decomposition(1) == []

def test_decompose_prime_two():
    # The prime number 2 yields a single factor: itself
    assert prime_factor_decomposition(2) == [2]

def test_decompose_prime_three():
    # The prime number 3 yields a single factor: itself
    assert prime_factor_decomposition(3) == [3]

def test_decompose_composite_four():
    # The composite number 4 yields its prime factors: 2 and 2
    # 2 * 2 = 4
    assert prime_factor_decomposition(4) == [2, 2]

def test_decompose_composite_six():
    # The composite number 6 yields its prime factors: 2 and 3
    # 2 * 3 = 6
    assert prime_factor_decomposition(6) == [2, 3]

def test_decompose_composite_eight():
    # The composite number 8 yields its prime factors: 2, 2, and 2
    # 2 * 2 * 2 = 8
    assert prime_factor_decomposition(8) == [2, 2, 2]

def test_decompose_composite_nine():
    # The composite number 9 yields its prime factors: 3 and 3
    # 3 * 3 = 9
    assert prime_factor_decomposition(9) == [3, 3]

def test_decompose_large_number():
    # The number 5 to the 9th power times 7 to the 13th power
    # 5^9 * 7^13 yields nine 5s followed by thirteen 7s
    expected_result = [5] * 9 + [7] * 13
    assert prime_factor_decomposition(5**9 * 7**13) == expected_result