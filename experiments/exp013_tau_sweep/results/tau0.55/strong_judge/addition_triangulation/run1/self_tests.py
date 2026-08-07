from solution import add_numbers

def test_add_two_positive_numbers():
    # Adding 3 and 5 yields 8
    assert add_numbers(3, 5) == 8

def test_add_two_other_positive_numbers():
    # Adding 4 and 7 yields 11
    assert add_numbers(4, 7) == 11

def test_add_negative_and_positive_number():
    # Adding -2 and 3 yields 1
    assert add_numbers(-2, 3) == 1

def test_add_two_negative_numbers():
    # Adding -4 and -6 yields -10
    assert add_numbers(-4, -6) == -10

def test_add_zero_and_positive_number():
    # Adding 0 and 5 yields 5
    assert add_numbers(0, 5) == 5

def test_add_zero_and_negative_number():
    # Adding 0 and -5 yields -5
    assert add_numbers(0, -5) == -5

def test_add_two_zeros():
    # Adding 0 and 0 yields 0
    assert add_numbers(0, 0) == 0