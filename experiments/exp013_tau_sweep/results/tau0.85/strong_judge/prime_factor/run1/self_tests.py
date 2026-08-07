from solution import prime_factors

def test_decomposing_number_one():
    # AC-1.1: The number 1 has no prime factors and yields the empty list.
    assert prime_factors(1) == []

def test_decomposing_prime_number_two():
    # AC-1.2: A prime number, 2 yields a single factor: itself.
    assert prime_factors(2) == [2]

def test_decomposing_prime_number_three():
    # AC-1.2: A prime number, 3 yields a single factor: itself.
    assert prime_factors(3) == [3]

def test_decomposing_composite_number_four():
    # AC-1.3: The number 4 is 2 * 2.
    assert prime_factors(4) == [2, 2]

def test_decomposing_composite_number_six():
    # AC-1.3: The number 6 is 2 * 3.
    assert prime_factors(6) == [2, 3]

def test_decomposing_composite_number_eight():
    # AC-1.3: The number 8 is 2 * 2 * 2.
    assert prime_factors(8) == [2, 2, 2]

def test_decomposing_composite_number_nine():
    # AC-1.3: The number 9 is 3 * 3.
    assert prime_factors(9) == [3, 3]

def test_decomposing_large_number():
    # AC-1.4: The number 5^9 * 7^13 = 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 * 5 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7 * 7
    assert prime_factors(5**9 * 7**13) == [5] * 9 + [7] * 13