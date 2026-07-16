from solution import add_two_numbers

def test_add_two_numbers_example_case():
    # Adding 3 and 5 yields 8
    result = add_two_numbers(3, 5)
    assert result == 8

def test_add_two_numbers_arbitrary_case_1():
    # Adding 4 and 7 yields 11
    result = add_two_numbers(4, 7)
    assert result == 11

def test_add_two_numbers_arbitrary_case_2():
    # Adding -1 and 1 yields 0
    result = add_two_numbers(-1, 1)
    assert result == 0

def test_add_two_numbers_arbitrary_case_3():
    # Adding 0 and 0 yields 0
    result = add_two_numbers(0, 0)
    assert result == 0

def test_add_two_numbers_arbitrary_case_4():
    # Adding -5 and -3 yields -8
    result = add_two_numbers(-5, -3)
    assert result == -8