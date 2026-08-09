import pytest
from solution import add_numbers

def test_empty_input_yields_zero():
    assert add_numbers("") == 0  # Empty input

def test_single_number_yields_value():
    assert add_numbers("2") == 2  # Single number
    assert add_numbers("0") == 0  # Zero as input

def test_numbers_separated_by_commas():
    assert add_numbers("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("10,20,30") == 60  # 10 + 20 + 30 = 60

def test_multi_line_input_with_line_breaks():
    assert add_numbers("1\n2") == 3  # 1 + 2 = 3
    assert add_numbers("1,2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("1\n2,3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_declaration():
    assert add_numbers("//;\n1;2") == 3  # 1 + 2 = 3 with custom delimiter ;
    assert add_numbers("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6 with custom delimiter *

def test_trailing_line_break_after_custom_delimited_numbers_is_insignificant():
    assert add_numbers("//;\n1;2\n") == 3  # 1 + 2 = 3 with custom delimiter ;
    
def test_zero_handling_with_custom_delimiter():
    assert add_numbers("//;\n0") == 0  # Zero with custom delimiter

def test_includes_number_1000_with_custom_delimiter():
    assert add_numbers("//;\n1000;1001") == 1000  # 1000 + 1001 (ignored) = 1000

def test_ignores_numbers_greater_than_1000():
    assert add_numbers("1000,1001") == 1000  # 1000 + 1001 (ignored) = 1000
    assert add_numbers("1,1001,2") == 3  # 1 + 2 (1001 ignored) = 3

def test_includes_number_1000():
    assert add_numbers("1000") == 1000  # Only 1000 present

def test_refuses_negative_numbers():
    with pytest.raises(BaseException) as excinfo:
        add_numbers("1,-2")
    assert str(excinfo.value) == "string contains -2, which does not meet rule. entered number should not negative."  # Negative number

    with pytest.raises(BaseException) as excinfo:
        add_numbers("-1,2")
    assert str(excinfo.value) == "string contains -1, which does not meet rule. entered number should not negative."  # Negative number

    with pytest.raises(BaseException) as excinfo:
        add_numbers("3,-4,5")
    assert str(excinfo.value) == "string contains -4, which does not meet rule. entered number should not negative."  # Negative number

def test_refuses_negative_numbers_with_custom_delimiter():
    with pytest.raises(BaseException) as excinfo:
        add_numbers("//;\n1;-2")
    assert str(excinfo.value) == "string contains -2, which does not meet rule. entered number should not negative."  # Negative number