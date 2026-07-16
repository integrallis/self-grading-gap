# test_calculator.py

from solution import add_numbers

def test_empty_input_yields_zero():
    # Empty input should yield 0
    assert add_numbers("") == 0

def test_single_number_yields_value():
    # Input "2" yields 2
    assert add_numbers("2") == 2
    # Input "0" yields 0
    assert add_numbers("0") == 0

def test_comma_separated_numbers():
    # Input "1,2,3" yields 1 + 2 + 3 = 6
    assert add_numbers("1,2,3") == 6
    # Input "5,10,15" yields 5 + 10 + 15 = 30
    assert add_numbers("5,10,15") == 30

def test_multi_line_input():
    # Input with line breaks should yield correct sum
    # "1\n2,3" yields 1 + 2 + 3 = 6
    assert add_numbers("1\n2,3") == 6
    # "4\n5\n6" yields 4 + 5 + 6 = 15
    assert add_numbers("4\n5\n6") == 15

def test_mixed_delimiters():
    # Input "1,2\n3" yields 1 + 2 + 3 = 6
    assert add_numbers("1,2\n3") == 6
    # Input "1\n2,3\n4" yields 1 + 2 + 3 + 4 = 10
    assert add_numbers("1\n2,3\n4") == 10

def test_custom_delimiter():
    # Input "//;\n1;2;3" uses ";" as delimiter and yields 1 + 2 + 3 = 6
    assert add_numbers("//;\n1;2;3") == 6
    # Input "//*\n1*2*3" uses "*" as delimiter and yields 1 + 2 + 3 = 6
    assert add_numbers("//*\n1*2*3") == 6

def test_custom_delimiter_zero_values():
    # Input "//;\n1;0;2" uses ";" as delimiter and yields 1 + 0 + 2 = 3
    assert add_numbers("//;\n1;0;2") == 3

def test_custom_delimiter_upper_limit():
    # Input "//;\n1000;1001" uses ";" as delimiter and yields 1000 (1001 is ignored)
    assert add_numbers("//;\n1000;1001") == 1000

def test_custom_delimiter_trailing_line_break():
    # Input "//;\n1;2\n" should yield 1 + 2 = 3, trailing line break is insignificant
    assert add_numbers("//;\n1;2\n") == 3

def test_ignore_oversized_numbers():
    # Input "1000,1001" yields 1000 (1001 is ignored)
    assert add_numbers("1000,1001") == 1000
    # Input "1000,2000,3000" yields 1000 (2000 and 3000 are ignored)
    assert add_numbers("1000,2000,3000") == 1000

def test_negative_numbers_refused():
    # Input "-1" should raise an error
    with pytest.raises(Exception) as exc_info:
        add_numbers("-1")
    assert str(exc_info.value) == "string contains -1, which does not meet rule. entered number should not negative."

    # Input "1,-2,3" should raise an error
    with pytest.raises(Exception) as exc_info:
        add_numbers("1,-2,3")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."

    # Input "//;\n1;-2;3" should raise an error
    with pytest.raises(Exception) as exc_info:
        add_numbers("//;\n1;-2;3")
    assert str(exc_info.value) == "string contains -2, which does not meet rule. entered number should not negative."