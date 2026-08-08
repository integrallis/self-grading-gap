from solution import add_text_numbers

def test_add_two_numeric_texts():
    # "1" + "2" = "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_numeric_text_and_empty():
    # "2" + "" = "2" (empty counts as zero)
    assert add_text_numbers("2", "") == "2"

def test_add_empty_and_numeric_text():
    # "" + "3" = "3" (empty counts as zero)
    assert add_text_numbers("", "3") == "3"

def test_add_two_empty_texts():
    # "" + "" = "0" (both empty count as zero)
    assert add_text_numbers("", "") == "0"

def test_add_large_numeric_texts():
    # "1000000" + "2000000" = "3000000"
    assert add_text_numbers("1000000", "2000000") == "3000000"