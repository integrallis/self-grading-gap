# test_calculator.py

from solution import add_numbers

def test_empty_input():
    # An empty input yields 0
    assert add_numbers("") == 0

def test_single_number():
    # A single number "2" yields 2
    assert add_numbers("2") == 2
    # A single number "0" yields 0
    assert add_numbers("0") == 0

def test_multiple_numbers_comma_separated():
    # "1,2,3" yields 6 (1 + 2 + 3)
    assert add_numbers("1,2,3") == 6
    # "10,20,30" yields 60 (10 + 20 + 30)
    assert add_numbers("10,20,30") == 60

def test_multiple_numbers_with_line_breaks():
    # "1\n2\n3" yields 6 (1 + 2 + 3)
    assert add_numbers("1\n2\n3") == 6
    # "1,2\n3" yields 6 (1 + 2 + 3)
    assert add_numbers("1,2\n3") == 6

def test_custom_delimiter():
    # "//;\n1;2;3" uses ";" as delimiter, yields 6 (1 + 2 + 3)
    assert add_numbers("//;\n1;2;3") == 6
    # "//*\n1*2*3" uses "*" as delimiter, yields 6 (1 + 2 + 3)
    assert add_numbers("//*\n1*2*3") == 6

def test_custom_delimiter_trailing_newline():
    # "//;\n1;2\n" uses ";" as delimiter, yields 3 (1 + 2)
    assert add_numbers("//;\n1;2\n") == 3

def test_custom_delimiter_zero_and_limit():
    # "//;\n0;1000;1001" yields 1000 (0 and 1000 included, 1001 ignored)
    assert add_numbers("//;\n0;1000;1001") == 1000

def test_ignored_numbers_above_1000():
    # "1001,2" yields 2 (1001 is ignored)
    assert add_numbers("1001,2") == 2
    # "1000,2" yields 1002 (1000 is included)
    assert add_numbers("1000,2") == 1002

def test_negative_numbers():
    # "-1" should raise an error
    with pytest.raises(ValueError) as excinfo:
        add_numbers("-1")
    assert str(excinfo.value) == "string contains -1, which does not meet rule. entered number should not negative."
    
    # "1,-2,3" should raise an error
    with pytest.raises(ValueError) as excinfo:
        add_numbers("1,-2,3")
    assert str(excinfo.value) == "string contains -2, which does not meet rule. entered number should not negative."

def test_mixed_input():
    # "1,-1000,1001" should raise an error for -1000
    with pytest.raises(ValueError) as excinfo:
        add_numbers("1,-1000,1001")
    assert str(excinfo.value) == "string contains -1000, which does not meet rule. entered number should not negative."
    
    # "1,2,1001,1000" yields 1003 (1001 is ignored)
    assert add_numbers("1,2,1001,1000") == 1003