# test_solution.py

from solution import add_numbers_from_text

def test_empty_input():
    # AC-1.1: Empty input yields a total of 0.
    assert add_numbers_from_text("") == 0

def test_single_number():
    # AC-1.2: Input holding a single number yields that number's value.
    assert add_numbers_from_text("2") == 2
    assert add_numbers_from_text("0") == 0

def test_multiple_numbers_comma_separated():
    # AC-1.3: Numbers separated by commas are all added together.
    assert add_numbers_from_text("1,2,3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers_from_text("10,20,30") == 60  # 10 + 20 + 30 = 60

def test_multi_line_input():
    # AC-2.1: A line break between two numbers separates them exactly like a comma.
    assert add_numbers_from_text("1\n2") == 3  # 1 + 2 = 3
    # AC-2.2: Commas and line breaks may be freely mixed within one input.
    assert add_numbers_from_text("1,2\n3") == 6  # 1 + 2 + 3 = 6

def test_custom_delimiter():
    # AC-3.1: Custom delimiter declaration at the start of the input.
    assert add_numbers_from_text("//;\n1;2;3") == 6  # 1 + 2 + 3 = 6
    assert add_numbers_from_text("//*\n1*2*3") == 6  # 1 + 2 + 3 = 6
    # AC-3.2: Trailing line break after numbers is insignificant.
    assert add_numbers_from_text("//;\n1;2;3\n") == 6  # 1 + 2 + 3 = 6
    # AC-3.3: Zero value under a custom delimiter.
    assert add_numbers_from_text("//;\n0;1") == 1  # 0 + 1 = 1
    # AC-3.3: Numbers greater than 1000 ignored under a custom delimiter.
    assert add_numbers_from_text("//;\n1000;1001") == 1000  # 1000 + 0 = 1000

def test_ignored_over_1000():
    # AC-4.1: Numbers greater than 1000 are ignored.
    assert add_numbers_from_text("1000,1001") == 1000  # 1000 + 0 = 1000
    assert add_numbers_from_text("100,2000,300") == 400  # 100 + 0 + 300 = 400

def test_includes_1000():
    # AC-4.2: The value 1000 itself is included in the total.
    assert add_numbers_from_text("1000") == 1000  # 1000 = 1000

def test_negative_values():
    # AC-4.3: Any negative number is refused with a specific message.
    try:
        add_numbers_from_text("-1")
    except Exception as e:
        assert str(e) == "string contains -1, which does not meet rule. entered number should not negative."
    
    try:
        add_numbers_from_text("1,-2,3")
    except Exception as e:
        assert str(e) == "string contains -2, which does not meet rule. entered number should not negative."
    
    try:
        add_numbers_from_text("//;\n1;-2")
    except Exception as e:
        assert str(e) == "string contains -2, which does not meet rule. entered number should not negative."