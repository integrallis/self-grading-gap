# test_calculator.py

from solution import add_numbers_from_delimited_text

def test_empty_input():
    # AC-1.1: Empty input yields 0
    assert add_numbers_from_delimited_text("") == 0

def test_single_number():
    # AC-1.2: Input holding a single number yields that number's value
    assert add_numbers_from_delimited_text("2") == 2
    assert add_numbers_from_delimited_text("0") == 0

def test_multiple_numbers_with_commas():
    # AC-1.3: Numbers separated by commas are added together
    assert add_numbers_from_delimited_text("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers_from_delimited_text("5,10,20") == 35  # 5 + 10 + 20 = 35

def test_multi_line_input():
    # AC-2.1: A line break between two numbers separates them like a comma
    assert add_numbers_from_delimited_text("1\n2") == 3  # 1 + 2 = 3
    assert add_numbers_from_delimited_text("1,2\n3") == 6  # 1 + 2 + 3 = 6

def test_mixed_delimiters():
    # AC-2.2: Commas and line breaks may be freely mixed
    assert add_numbers_from_delimited_text("1,2\n3,4") == 10  # 1 + 2 + 3 + 4 = 10

def test_custom_delimiter():
    # AC-3.1: Custom delimiter declaration works
    assert add_numbers_from_delimited_text("//;\n1;2") == 3  # 1 + 2 = 3
    assert add_numbers_from_delimited_text("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_with_newlines():
    # AC-3.2: Delimiter declaration ends at first line break
    assert add_numbers_from_delimited_text("//;\n1;2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers_from_delimited_text("//;\n1;2;1001") == 3  # 1 + 2 + 1001 (ignored) = 3

def test_negative_numbers():
    # AC-4.3: Negative number is refused with the correct message
    try:
        add_numbers_from_delimited_text("-1,2")
    except ValueError as e:
        assert str(e) == "string contains -1, which does not meet rule. entered number should not negative."

def test_ignore_oversized_values():
    # AC-4.1: Numbers greater than 1000 are ignored
    assert add_numbers_from_delimited_text("1001,2") == 2  # 1001 is ignored, so total is 2
    assert add_numbers_from_delimited_text("1000,2") == 1002  # 1000 is included, so total is 1002

def test_multiple_oversized_values():
    # Multiple oversized values in one input
    assert add_numbers_from_delimited_text("1000,1001,2000") == 1000  # Only 1000 is included