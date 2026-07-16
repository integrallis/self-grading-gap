from solution import prime_factor_decomposition

def test_decomposing_number_one():
    # AC-1.1: The number 1 has no prime factors and yields the empty list.
    assert prime_factor_decomposition(1) == []

def test_decomposing_prime_number_two():
    # AC-1.2: A prime number yields a single factor: itself; 2 yields 2.
    assert prime_factor_decomposition(2) == [2]

def test_decomposing_prime_number_three():
    # AC-1.2: A prime number yields a single factor: itself; 3 yields 3.
    assert prime_factor_decomposition(3) == [3]

def test_decomposing_composite_number_four():
    # AC-1.3: A composite number yields its prime factors; 4 yields 2 and 2.
    assert prime_factor_decomposition(4) == [2, 2]

def test_decomposing_composite_number_six():
    # AC-1.3: A composite number yields its prime factors; 6 yields 2 and 3.
    assert prime_factor_decomposition(6) == [2, 3]

def test_decomposing_composite_number_eight():
    # AC-1.3: A composite number yields its prime factors; 8 yields 2, 2, and 2.
    assert prime_factor_decomposition(8) == [2, 2, 2]

def test_decomposing_composite_number_nine():
    # AC-1.3: A composite number yields its prime factors; 9 yields 3 and 3.
    assert prime_factor_decomposition(9) == [3, 3]

def test_decomposing_large_composite_number():
    # AC-1.4: 5^9 * 7^13 yields nine 5s followed by thirteen 7s.
    # 5^9 = 5, 5, 5, 5, 5, 5, 5, 5, 5
    # 7^13 = 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
    expected_result = [5] * 9 + [7] * 13
    assert prime_factor_decomposition(5**9 * 7**13) == expected_result