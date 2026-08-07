from solution import add_text_numbers

def test_add_two_numeric_texts():
    # "1" + "2" = 3
    assert add_text_numbers("1", "2") == "3"

def test_add_numeric_text_and_empty():
    # "1" + "" = 1 (empty counts as 0)
    assert add_text_numbers("1", "") == "1"

def test_add_empty_and_numeric_text():
    # "" + "2" = 2 (empty counts as 0)
    assert add_text_numbers("", "2") == "2"

def test_add_two_empty_texts():
    # "" + "" = 0 (both empty count as 0)
    assert add_text_numbers("", "") == "0"