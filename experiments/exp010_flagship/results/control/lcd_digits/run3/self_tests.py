from solution import render_digit, render_number

def test_render_single_digit_0():
    # The digit 0 should render as:
    # ._.
    # |.|
    # |_|
    expected_output = "._.\n|.|\n|_|\n"
    assert render_digit(0) == expected_output

def test_render_single_digit_1():
    # The digit 1 should render as:
    # ...
    # ..|
    # ..|
    expected_output = "...\n..|\n..|\n"
    assert render_digit(1) == expected_output

def test_render_multi_digit_10():
    # The number 10 should render by concatenating the renderings of 1 and 0:
    # 1:
    # ...
    # ..|
    # ..|
    #
    # 0:
    # ._.
    # |.|
    # |_|
    expected_output = "...._.\n..||.|\n..||_|\n"
    assert render_number(10) == expected_output

def test_render_multi_digit_100():
    # The number 100 should render by concatenating the renderings of 1, 0, and 0:
    # 1:
    # ...
    # ..|
    # ..|
    #
    # 0:
    # ._.
    # |.|
    # |_|
    #
    # 0:
    # ._.
    # |.|
    # |_|
    expected_output = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_number(100) == expected_output