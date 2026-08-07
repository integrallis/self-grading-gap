from solution import add_numbers_as_text

def test_add_two_numeric_texts():
    # "1" and "2" yield "3"
    assert add_numbers_as_text("1", "2") == "3"

def test_add_second_numeric_text_case():
    # "12" and "34" yield "46"
    assert add_numbers_as_text("12", "34") == "46"

def test_add_numeric_text_and_empty():
    # "5" and "" yield "5" (empty counts as zero)
    assert add_numbers_as_text("5", "") == "5"

def test_add_empty_and_numeric_text():
    # "" and "3" yield "3" (empty counts as zero)
    assert add_numbers_as_text("", "3") == "3"

def test_add_two_empty_texts():
    # "" and "" yield "0" (both empty count as zero)
    assert add_numbers_as_text("", "") == "0"