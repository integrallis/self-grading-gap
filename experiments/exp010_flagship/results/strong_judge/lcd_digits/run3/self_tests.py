# your complete test file
from solution import function_name  # Replace function_name with the correct public API name

def test_render_single_digit_0():
    # Expected rendering of '0':
    expected = "._.\n|.|\n|_|\n"  # Three lines with newline characters
    assert function_name(0) == expected

def test_render_single_digit_1():
    # Expected rendering of '1':
    expected = "...\n..|\n..|\n"  # Three lines with newline characters
    assert function_name(1) == expected

def test_render_multi_digit_10():
    # Expected rendering of '10':
    expected = "...._.\n..||.|\n..||_|\n"  # Concatenation of '1' and '0'
    assert function_name(10) == expected

def test_render_multi_digit_100():
    # Expected rendering of '100':
    expected = "...._.._.\n..||.||.|\n..||_||_|\n"  # Concatenation of '1', '0', and '0'
    assert function_name(100) == expected

def test_render_multi_digit_101():
    # Expected rendering of '101':
    expected = "...._....\n..||.|..|\n..||_|..|\n"  # Concatenation of '1', '0', and '1'
    assert function_name(101) == expected