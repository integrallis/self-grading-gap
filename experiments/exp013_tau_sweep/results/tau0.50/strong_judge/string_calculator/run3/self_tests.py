import pytest
from solution import add_numbers_from_text

def test_empty_input():
    # An empty input yields 0
    assert add_numbers_from_text("") == 0

def test_single_number():
    # A single number "2" yields 2
    assert add_numbers_from_text("2") == 2
    # A single number "0" yields 0
    assert add_numbers_from_text("0") == 0

def test_multiple_numbers_with_commas():
    # "1,2,3" yields 1 + 2 + 3 = 6
    assert add_numbers_from_text("1,2,3") == 6
    # "10,20,30" yields 10 + 20 + 30 = 60
    assert add_numbers_from_text("10,20,30") == 60

def test_multiline_input():
    # "1\n2" yields 1 + 2 = 3 (line break treated like a comma)
    assert add_numbers_from_text("1\n2") == 3
    # "1,2\n3" yields 1 + 2 + 3 = 6 (mixed delimiters)
    assert add_numbers_from_text("1,2\n3") == 6

def test_custom_delimiter():
    # "//;\n1;2" uses ";" as a delimiter, yields 1 + 2 = 3
    assert add_numbers_from_text("//;\n1;2") == 3
    # "//*\n1*2*3" uses "*" as a delimiter, yields 1 + 2 + 3 = 6
    assert add_numbers_from_text("//*\n1*2*3") == 6
    # "//;\n1;2\n" with trailing newline yields 1 + 2 = 3
    assert add_numbers_from_text("//;\n1;2\n") == 3
    # "//;\n0;2" uses ";" as a delimiter, yields 0 + 2 = 2
    assert add_numbers_from_text("//;\n0;2") == 2
    # "//;\n1000;1001" uses ";" as a delimiter, yields 1000 (1001 is ignored)
    assert add_numbers_from_text("//;\n1000;1001") == 1000
    # "//;\n1;-2" should raise an error for -2
    with pytest.raises(BaseException) as exc_info:
        add_numbers_from_text("//;\n1;-2")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."

def test_ignore_large_numbers():
    # "1000,1001" yields 1000 (1001 is ignored)
    assert add_numbers_from_text("1000,1001") == 1000
    # "1001,999" yields 999 (1001 is ignored)
    assert add_numbers_from_text("1001,999") == 999

def test_negative_numbers():
    # "-1" should raise an error
    with pytest.raises(BaseException) as exc_info:
        add_numbers_from_text("-1")
    assert str(exc_info.value) == "string contains -1, which does not meet rule. entered number should not negative."
    
    # "1,-2,3" should raise an error for -2
    with pytest.raises(BaseException) as exc_info:
        add_numbers_from_text("1,-2,3")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."

def test_ignore_negative_and_large_numbers():
    # "1000,-1,1001" should raise an error for -1
    with pytest.raises(BaseException) as exc_info:
        add_numbers_from_text("1000,-1,1001")
    assert str(exc_info.value) == "string contains -1, which does not meet rule. entered number should not negative."

def test_mixed_delimiters_with_negatives():
    # "1,-2\n3" should raise an error for -2
    with pytest.raises(BaseException) as exc_info:
        add_numbers_from_text("1,-2\n3")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."