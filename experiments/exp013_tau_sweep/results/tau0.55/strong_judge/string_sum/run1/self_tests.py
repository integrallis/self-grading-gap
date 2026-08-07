from solution import add_text_numbers

def test_add_two_numeric_texts():
    # "1" + "2" = 3
    assert add_text_numbers("1", "2") == "3"

def test_add_text_number_and_empty():
    # "5" + "" = 5 (empty counts as 0)
    assert add_text_numbers("5", "") == "5"
    
def test_add_empty_and_text_number():
    # "" + "7" = 7 (empty counts as 0)
    assert add_text_numbers("", "7") == "7"

def test_add_two_empty_texts():
    # "" + "" = 0 (both empty count as 0)
    assert add_text_numbers("", "") == "0"
    
def test_add_zero_and_text_number():
    # "0" + "3" = 3
    assert add_text_numbers("0", "3") == "3"

def test_add_text_number_and_zero():
    # "4" + "0" = 4
    assert add_text_numbers("4", "0") == "4"

def test_add_two_digit_numeric_texts():
    # "12" + "34" = 46
    assert add_text_numbers("12", "34") == "46"

def test_add_large_numeric_texts():
    # "99" + "1" = 100
    assert add_text_numbers("99", "1") == "100"