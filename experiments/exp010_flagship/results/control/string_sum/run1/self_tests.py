# test_solution.py

from solution import add_text_numbers

def test_add_text_numbers_two_numeric_texts():
    # "1" + "2" = "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_text_numbers_empty_first_operand():
    # "" + "2" = "2" (empty counts as 0)
    assert add_text_numbers("", "2") == "2"

def test_add_text_numbers_empty_second_operand():
    # "1" + "" = "1" (empty counts as 0)
    assert add_text_numbers("1", "") == "1"

def test_add_text_numbers_both_empty_operands():
    # "" + "" = "0" (both empty count as 0)
    assert add_text_numbers("", "") == "0"