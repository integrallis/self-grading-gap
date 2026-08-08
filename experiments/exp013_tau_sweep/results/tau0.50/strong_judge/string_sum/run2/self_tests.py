def test_add_two_numeric_texts():
    # Test AC-1.1: "1" and "2" yield "3"
    assert add_text_numbers("1", "2") == "3"

def test_add_two_numeric_texts_another_case():
    # Test AC-1.1: "12" and "34" yield "46"
    assert add_text_numbers("12", "34") == "46"

def test_add_empty_operand():
    # Test AC-1.2: An empty operand counts as zero, result should be "2"
    assert add_text_numbers("", "2") == "2"

def test_add_empty_operand_second():
    # Test AC-1.2: An empty second operand counts as zero, result should be "2"
    assert add_text_numbers("2", "") == "2"

def test_add_two_empty_operands():
    # Test AC-1.3: Both operands are empty, result should be "0"
    assert add_text_numbers("", "") == "0"

# The tests for None inputs have been removed as they are not specified in the requirements.