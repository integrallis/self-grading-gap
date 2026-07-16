from solution import add_numbers

def test_add_two_numbers_example():
    # Adding 3 and 5 yields 8
    assert add_numbers(3, 5) == 8

def test_add_two_numbers_arbitrary():
    # For any two integers, the result equals their arithmetic sum.
    assert add_numbers(4, 7) == 11  # 4 + 7 = 11
    assert add_numbers(-1, 1) == 0   # -1 + 1 = 0
    assert add_numbers(-5, -3) == -8  # -5 + -3 = -8
    assert add_numbers(0, 0) == 0    # 0 + 0 = 0
    assert add_numbers(10, 15) == 25  # 10 + 15 = 25