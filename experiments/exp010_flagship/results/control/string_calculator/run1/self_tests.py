# test_solution.py

from solution import add_numbers_from_text

def test_empty_input():
    # AC-1.1: Empty input yields 0
    assert add_numbers_from_text("") == 0

def test_single_number():
    # AC-1.2: Input holding a single number yields that number's value
    assert add_numbers_from_text("2") == 2
    assert add_numbers_from_text("0") == 0

def test_multiple_numbers():
    # AC-1.3: Numbers separated by commas are all added together
    assert add_numbers_from_text("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers_from_text("0,0,0") == 0  # 0 + 0 + 0 = 0

def test_multi_line_input():
    # AC-2.1: A line break between two numbers separates them exactly like a comma
    assert add_numbers_from_text("1\n2") == 3  # 1 + 2 = 3
    # AC-2.2: Commas and line breaks may be freely mixed within one input
    assert add_numbers_from_text("1,2\n3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter():
    # AC-3.1: Declaring a custom delimiter
    assert add_numbers_from_text("//;\n1;2") == 3  # 1 + 2 = 3
    assert add_numbers_from_text("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6
    # AC-3.2: The delimiter declaration ends at the first line break
    assert add_numbers_from_text("//;\n1;2;\n") == 3  # 1 + 2 = 3

def test_out_of_range_and_negative_values():
    # AC-4.1: Numbers greater than 1000 are ignored
    assert add_numbers_from_text("1001,2") == 2  # 2 is added, 1001 is ignored
    assert add_numbers_from_text("1000,1") == 1001  # 1000 is included, 1 is added
    # AC-4.3: Any negative number is refused
    try:
        add_numbers_from_text("-1")
    except ValueError as e:
        assert str(e) == "string contains -1, which does not meet rule. entered number should not negative."
    
    try:
        add_numbers_from_text("2,-3,5")
    except ValueError as e:
        assert str(e) == "string contains -3, which does not meet rule. entered number should not negative."