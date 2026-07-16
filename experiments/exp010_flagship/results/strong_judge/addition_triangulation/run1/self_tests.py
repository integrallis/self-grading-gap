# test_adder.py

from solution import add_two_numbers

def test_add_two_numbers_example_case():
    # Adding 3 and 5 yields 8
    assert add_two_numbers(3, 5) == 8

def test_add_two_numbers_arbitrary_case():
    # For any two integers, the result equals their arithmetic sum
    assert add_two_numbers(4, 7) == 11