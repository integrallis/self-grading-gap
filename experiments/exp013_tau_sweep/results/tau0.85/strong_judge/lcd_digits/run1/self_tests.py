from solution import render_digit, render_number

def test_render_digit_0():
    # The digit 0 should render as:
    # ._.
    # |.|
    # |_|
    expected_output = "._.\n|.|\n|_|\n"
    assert render_digit(0) == expected_output

def test_render_digit_1():
    # The digit 1 should render as:
    # ...
    # ..|
    # ..|
    expected_output = "...\n..|\n..|\n"
    assert render_digit(1) == expected_output

def test_render_number_10():
    # The number 10 should render as:
    # ...._.
    # ..||.|
    # ..||_|
    expected_output = "...._.\n..||.|\n..||_|\n"
    assert render_number(10) == expected_output

def test_render_number_100():
    # The number 100 should render as:
    # ...._.._.
    # ..||.||.|
    # ..||_||_|
    expected_output = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_number(100) == expected_output

def test_render_number_101():
    # The number 101 should render as:
    # ...._....
    # ..||.|..|
    # ..||_|..|
    expected_output = "...._....\n..||.|..|\n..||_|..|\n"
    assert render_number(101) == expected_output