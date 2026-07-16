from solution import add_two_numbers

def test_add_two_numbers_example_case():
    # Adding 3 and 5 yields 8
    assert add_two_numbers(3, 5) == 8

def test_add_two_numbers_arbitrary_case():
    # Adding 4 and 7 yields 11
    assert add_two_numbers(4, 7) == 11

def test_add_two_numbers_negative_case():
    # Adding -2 and 5 yields 3
    assert add_two_numbers(-2, 5) == 3

def test_add_two_numbers_zero_case():
    # Adding 0 and 0 yields 0
    assert add_two_numbers(0, 0) == 0

def test_add_two_numbers_large_numbers():
    # Adding 1000 and 2000 yields 3000
    assert add_two_numbers(1000, 2000) == 3000

def test_add_two_numbers_negative_and_positive():
    # Adding -3 and 3 yields 0
    assert add_two_numbers(-3, 3) == 0

def test_add_two_numbers_large_negative_numbers():
    # Adding -1000 and -2000 yields -3000
    assert add_two_numbers(-1000, -2000) == -3000