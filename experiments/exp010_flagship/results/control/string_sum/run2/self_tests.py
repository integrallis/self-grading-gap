from solution import add_numeric_texts

def test_add_numeric_texts_two_numeric_texts():
    # "1" + "2" = "3"
    assert add_numeric_texts("1", "2") == "3"

def test_add_numeric_texts_first_operand_empty():
    # "" + "2" counts as 0 + 2 = "2"
    assert add_numeric_texts("", "2") == "2"

def test_add_numeric_texts_second_operand_empty():
    # "1" + "" counts as 1 + 0 = "1"
    assert add_numeric_texts("1", "") == "1"

def test_add_numeric_texts_both_operands_empty():
    # "" + "" counts as 0 + 0 = "0"
    assert add_numeric_texts("", "") == "0"