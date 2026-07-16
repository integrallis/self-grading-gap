from solution import add_numbers

def test_empty_input():
    # AC-1.1: Empty input yields 0
    assert add_numbers("") == 0

def test_single_number():
    # AC-1.2: Single number input yields that number
    assert add_numbers("0") == 0
    assert add_numbers("2") == 2
    assert add_numbers("1000") == 1000

def test_multiple_numbers_with_commas():
    # AC-1.3: Numbers separated by commas are added together
    assert add_numbers("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("10,20,30") == 60  # 10 + 20 + 30 = 60
    assert add_numbers("100,200,300") == 600  # 100 + 200 + 300 = 600

def test_multi_line_input():
    # AC-2.1: Line breaks separate numbers like commas
    assert add_numbers("1\n2") == 3  # 1 + 2 = 3
    assert add_numbers("1,2\n3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("1\n2,3") == 6  # 1 + 2 + 3 = 6

def test_mixed_delimiters():
    # AC-2.2: Commas and line breaks may be freely mixed
    assert add_numbers("1,2\n3,4\n5") == 15  # 1 + 2 + 3 + 4 + 5 = 15

def test_custom_delimiter():
    # AC-3.1: Custom delimiter declared with two slashes
    assert add_numbers("//;\n1;2;3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter_with_mixed_input():
    # AC-3.2: Custom delimiter with mixed commas and line breaks
    assert add_numbers("//;\n1;2,3\n4") == 10  # 1 + 2 + 3 + 4 = 10

def test_ignored_values():
    # AC-4.1: Numbers greater than 1000 are ignored
    assert add_numbers("2,1001") == 2  # 2 + 1001 (ignored) = 2
    assert add_numbers("1000,1001") == 1000  # 1000 + 1001 (ignored) = 1000

def test_inclusive_upper_limit():
    # AC-4.2: The value 1000 itself is included
    assert add_numbers("1000") == 1000  # 1000 = 1000

def test_negative_values():
    # AC-4.3: Negative numbers are rejected with a specific message
    try:
        add_numbers("-1")
    except ValueError as e:
        assert str(e) == "string contains -1, which does not meet rule. entered number should not negative."

    try:
        add_numbers("2,-5,3")
    except ValueError as e:
        assert str(e) == "string contains -5, which does not meet rule. entered number should not negative."