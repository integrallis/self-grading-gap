from solution import add_text_numbers

def test_add_two_numeric_texts():
    # "1" and "2" yield "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_numeric_text_and_empty():
    # "1" and "" count as "1" and "0", yield "1"
    assert add_text_numbers("1", "") == "1"

def test_add_empty_and_numeric_text():
    # "" and "2" count as "0" and "2", yield "2"
    assert add_text_numbers("", "2") == "2"

def test_add_two_empty_texts():
    # "" and "" count as "0" and "0", yield "0"
    assert add_text_numbers("", "") == "0"

def test_add_numeric_texts_with_zero():
    # "0" and "2" yield "2"
    assert add_text_numbers("0", "2") == "2"

def test_add_texts_with_leading_trailing_spaces():
    # " 1 " and " 2 " should be treated as "1" and "2", yield "3"
    assert add_text_numbers(" 1 ", " 2 ") == "3"