# test_solution.py

from solution import add_text_numbers

def test_add_two_numeric_texts():
    # AC-1.1: "1" + "2" = "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_numeric_text_and_empty():
    # AC-1.2: "5" + "" = "5" (empty counts as 0)
    assert add_text_numbers("5", "") == "5"

def test_add_empty_and_numeric_text():
    # AC-1.2: "" + "3" = "3" (empty counts as 0)
    assert add_text_numbers("", "3") == "3"

def test_add_two_empty_texts():
    # AC-1.3: "" + "" = "0" (both empty counts as 0)
    assert add_text_numbers("", "") == "0"

def test_add_two_numeric_texts_with_zero():
    # AC-1.1: "0" + "0" = "0"
    assert add_text_numbers("0", "0") == "0"