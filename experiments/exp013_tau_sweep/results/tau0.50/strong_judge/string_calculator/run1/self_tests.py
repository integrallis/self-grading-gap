# test_solution.py

from solution import add_numbers  # Assuming the public API is defined by the implementer

def test_empty_input():
    # Empty input yields 0
    assert add_numbers("") == 0

def test_single_number():
    # Input holding a single number yields that number's value
    assert add_numbers("2") == 2  # Single number 2
    assert add_numbers("0") == 0  # Single number 0

def test_multiple_numbers_commas():
    # Numbers separated by commas are all added together
    assert add_numbers("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("10,20,30") == 60  # 10 + 20 + 30 = 60

def test_multi_line_input():
    # A line break between two numbers separates them exactly like a comma
    assert add_numbers("1\n2") == 3  # 1 + 2 = 3
    assert add_numbers("1,2\n3") == 6  # 1 + 2 + 3 = 6

def test_mixed_delimiters():
    # Commas and line breaks may be freely mixed within one input
    assert add_numbers("1,2\n3,4") == 10  # 1 + 2 + 3 + 4 = 10

def test_custom_delimiter():
    # An input beginning with two slashes, a single delimiter character, and a line break
    assert add_numbers("//;\n1;2;3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_with_mixed():
    # The delimiter declaration ends at the first line break
    assert add_numbers("//;\n1;2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("//;\n0;1000;1001") == 1000  # 0 + 1000 + ignored(1001) = 1000

def test_trailing_newline_custom_delimiter():
    # Trailing line break after custom-delimited numbers is insignificant
    assert add_numbers("//;\n1;2\n") == 3  # 1 + 2 = 3

def test_ignores_oversized_values():
    # Numbers greater than 1000 are ignored and contribute nothing to the total
    assert add_numbers("1000,1001") == 1000  # 1000 is included, 1001 is ignored

def test_includes_1000():
    # The value 1000 itself is included in the total
    assert add_numbers("1000") == 1000  # Single number 1000

def test_refuses_negative_numbers():
    # Any negative number is refused
    try:
        add_numbers("-1")
    except ValueError as e:
        assert str(e) == "string contains -1, which does not meet rule. entered number should not negative."  # Negative value
    
    try:
        add_numbers("5,-2,3")
    except ValueError as e:
        assert str(e) == "string contains -2, which does not meet rule. entered number should not negative."  # Negative value