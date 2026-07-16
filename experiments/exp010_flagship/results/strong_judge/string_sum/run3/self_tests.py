from solution import add_text_numbers

def test_add_two_numeric_texts():
    # "1" + "2" = "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_empty_and_numeric_text():
    # "" + "5" = "5" (empty counts as 0)
    assert add_text_numbers("", "5") == "5"

def test_add_numeric_text_and_empty():
    # "3" + "" = "3" (empty counts as 0)
    assert add_text_numbers("3", "") == "3"

def test_add_two_empty_texts():
    # "" + "" = "0" (both empty count as 0)
    assert add_text_numbers("", "") == "0"

def test_add_numeric_texts_with_zero():
    # "0" + "7" = "7"
    assert add_text_numbers("0", "7") == "7"

# Future tests for missing operands will be added once the representation is specified.