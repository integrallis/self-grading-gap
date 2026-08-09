import pytest
from solution import add_numbers

def test_empty_input():
    # AC-1.1: Empty input yields 0
    assert add_numbers("") == 0

def test_single_number():
    # AC-1.2: Input holding a single number yields that number's value
    assert add_numbers("2") == 2
    assert add_numbers("0") == 0

def test_multiple_numbers_comma_separated():
    # AC-1.3: Numbers separated by commas are added together
    assert add_numbers("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("10,20,30") == 60  # 10 + 20 + 30 = 60

def test_multiple_numbers_with_line_breaks():
    # AC-2.1: A line break between two numbers separates them
    assert add_numbers("1\n2") == 3  # 1 + 2 = 3
    assert add_numbers("1,\n2") == 3  # 1 + 2 = 3

def test_mixed_delimiters():
    # AC-2.2: Commas and line breaks may be freely mixed
    assert add_numbers("1,2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("1\n2,3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter():
    # AC-3.1: Custom delimiter declared
    assert add_numbers("//;\n1;2") == 3  # 1 + 2 = 3
    assert add_numbers("//*\n3*4*5") == 12  # 3 + 4 + 5 = 12

def test_custom_delimiter_with_line_break():
    # AC-3.2: Delimiter declaration ends at the first line break
    assert add_numbers("//;\n1;2\n3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_ignores_trailing_line_break():
    # AC-3.2: Trailing line break after numbers is insignificant
    assert add_numbers("//;\n1;2\n") == 3  # 1 + 2 = 3

def test_zero_with_custom_delimiter():
    # Verify zero values under a custom delimiter
    assert add_numbers("//;\n0;1") == 1  # 0 + 1 = 1

def test_ignore_large_numbers():
    # AC-4.1: Numbers greater than 1000 are ignored
    assert add_numbers("1001,2") == 2  # 1001 is ignored, so total is 2
    assert add_numbers("1000,1001") == 1000  # 1001 is ignored, total is 1000

def test_include_exactly_1000():
    # AC-4.2: The value 1000 itself is included in the total
    assert add_numbers("1000") == 1000  # Total is 1000

def test_custom_delimiter_ignore_large_numbers():
    # Verify custom delimiter upper-limit boundaries
    assert add_numbers("//;\n1000;1001;2") == 1002  # 1001 is ignored, total is 1002

def test_negative_numbers():
    # AC-4.3: Any negative number is refused
    with pytest.raises(BaseException, match=r"^string contains -1, which does not meet rule\. entered number should not negative\.$"):
        add_numbers("-1")
    
    with pytest.raises(BaseException, match=r"^string contains -2, which does not meet rule\. entered number should not negative\.$"):
        add_numbers("1,-2,3")