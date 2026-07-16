from solution import add_numbers_as_text  # Import the function from the solution package

def test_add_two_numeric_texts():
    # Adding "1" and "2" should yield "3"
    assert add_numbers_as_text("1", "2") == "3"

def test_add_numeric_text_and_empty():
    # Adding "5" and empty string should yield "5"
    assert add_numbers_as_text("5", "") == "5"  # empty counts as zero
    # Adding empty and "3" should yield "3"
    assert add_numbers_as_text("", "3") == "3"  # empty counts as zero

def test_add_two_empty_texts():
    # Adding empty and empty should yield "0"
    assert add_numbers_as_text("", "") == "0"  # both empty count as zero

def test_add_numeric_text_and_missing_first():
    # Adding missing first operand (None) and "2" should yield "2"
    assert add_numbers_as_text(None, "2") == "2"  # missing counts as zero

def test_add_numeric_text_and_missing_second():
    # Adding "5" and missing second operand (None) should yield "5"
    assert add_numbers_as_text("5", None) == "5"  # missing counts as zero

def test_add_two_missing_operands():
    # Adding missing first and second operands (both None) should yield "0"
    assert add_numbers_as_text(None, None) == "0"  # both missing count as zero