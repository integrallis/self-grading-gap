import pytest
from solution import add_numbers

def test_empty_input():
    # Empty input yields 0
    assert add_numbers("") == 0

def test_absent_input():
    # Absent input yields 0
    assert add_numbers(None) == 0

def test_single_number():
    # Input holding a single number yields that number's value
    assert add_numbers("2") == 2
    assert add_numbers("0") == 0

def test_multiple_numbers_with_commas():
    # Numbers separated by commas are all added together
    assert add_numbers("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("10,20,30") == 60  # 10 + 20 + 30 = 60

def test_multi_line_input():
    # Line breaks act as separators alongside commas
    assert add_numbers("1,2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("1\n2,3") == 6  # 1 + 2 + 3 = 6

def test_mixed_commas_and_line_breaks():
    # Commas and line breaks may be freely mixed within one input
    assert add_numbers("1,\n2,3\n4") == 10  # 1 + 2 + 3 + 4 = 10

def test_custom_delimiter():
    # Custom delimiter declared at the start of the input
    assert add_numbers("//;\n1;2") == 3  # 1 + 2 = 3
    assert add_numbers("//*\n3*4*5") == 12  # 3 + 4 + 5 = 12

def test_custom_delimiter_with_line_break():
    # Delimiter declaration ends at the first line break
    assert add_numbers("//;\n1;2\n3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_with_trailing_break():
    # Trailing line break after numbers is insignificant
    assert add_numbers("//;\n1;2\n") == 3  # 1 + 2 = 3

def test_zero_with_custom_delimiter():
    # Zero remains valid with a custom delimiter
    assert add_numbers("//;\n0;1") == 1  # 0 + 1 = 1

def test_ignore_oversized_values():
    # Numbers greater than 1000 are ignored
    assert add_numbers("1000,1001") == 1000  # 1000 + 0 = 1000
    assert add_numbers("2000,3000") == 0  # 0

def test_include_1000_in_total():
    # The value 1000 itself is included in the total
    assert add_numbers("1000") == 1000  # 1000 = 1000
    assert add_numbers("//;\n1000;1001") == 1000  # 1000 + 0 = 1000

def test_refuse_negative_values():
    # Negative numbers are refused with error message
    with pytest.raises(Exception) as exc_info:
        add_numbers("-1")
    assert str(exc_info.value) == "string contains -1, which does not meet rule. entered number should not negative."
    
    with pytest.raises(Exception) as exc_info:
        add_numbers("2,-2")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."
    
    with pytest.raises(Exception) as exc_info:
        add_numbers("//;\n1;2;-5")
    assert str(exc_info.value) == "string contains -5, which does not meet rule. entered number should not negative."