# your complete test file
import pytest
from solution import add_numbers

def test_empty_input():
    # An empty input should yield a total of 0.
    assert add_numbers("") == 0

def test_single_number():
    # A single number input "2" yields 2.
    assert add_numbers("2") == 2
    # A single number input "0" yields 0.
    assert add_numbers("0") == 0

def test_multiple_numbers_with_commas():
    # Input "1,2,3" yields 1 + 2 + 3 = 6.
    assert add_numbers("1,2,3") == 6
    # Input "5,10,15" yields 5 + 10 + 15 = 30.
    assert add_numbers("5,10,15") == 30

def test_multi_line_input():
    # Input "1\n2\n3" (1, 2, and 3 on different lines) yields 1 + 2 + 3 = 6.
    assert add_numbers("1\n2\n3") == 6
    # Input "1,2\n3,4" yields 1 + 2 + 3 + 4 = 10.
    assert add_numbers("1,2\n3,4") == 10

def test_custom_delimiter():
    # Input "//;\n1;2" declares ';' and yields 1 + 2 = 3.
    assert add_numbers("//;\n1;2") == 3
    # Input "//*\n1*2*3" declares '*' and yields 1 + 2 + 3 = 6.
    assert add_numbers("//*\n1*2*3") == 6
    # Input "//;\n1;2;3\n4" yields 1 + 2 + 3 + 4 = 10.
    assert add_numbers("//;\n1;2;3\n4") == 10
    # Verify that a trailing line break after custom-delimited numbers is insignificant.
    assert add_numbers("//;\n1;2\n") == 3
    # Verify zero handling with a custom delimiter.
    assert add_numbers("//;\n0;1") == 1
    # Verify both the 1000 boundary and oversized-value exclusion with a custom delimiter.
    assert add_numbers("//;\n1000;1001") == 1000

def test_ignore_oversized_values():
    # Input "2,1001" ignores 1001, yielding 2.
    assert add_numbers("2,1001") == 2
    # Input "1000,1001" includes 1000, ignores 1001, yielding 1000.
    assert add_numbers("1000,1001") == 1000

def test_refuse_negative_values():
    # Input "1,-2" should raise an error with the specified message.
    with pytest.raises(Exception) as exc_info:
        add_numbers("1,-2")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."
    
    # Input "-1,2" should raise an error with the specified message.
    with pytest.raises(Exception) as exc_info:
        add_numbers("-1,2")
    assert str(exc_info.value) == "string contains -1, which does not meet rule. entered number should not negative."
    
    # Input "3,-4,5" should raise an error with the specified message for -4.
    with pytest.raises(Exception) as exc_info:
        add_numbers("3,-4,5")
    assert str(exc_info.value) == "string contains -4, which does not meet rule. entered number should not negative."
    
    # Custom delimiter negative test
    with pytest.raises(Exception) as exc_info:
        add_numbers("//;\n1;-2")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."