from solution import render_digit

def test_render_single_digit_0():
    # Expected output for digit 0:
    expected = "._.\n|.|\n|_|\n"
    assert render_digit(0) == expected

def test_render_single_digit_1():
    # Expected output for digit 1:
    expected = "...\n..|\n..|\n"
    assert render_digit(1) == expected

def test_render_multi_digit_10():
    # Expected output for number 10:
    # First digit (1):
    # ...
    # ..|
    # ..|
    # Second digit (0):
    # ._.
    # |.|
    # |_|
    # corresponds to:
    # ...._.
    # ..||.|
    # ..||_|
    expected = "...._.\n..||.|\n..||_|\n"
    assert render_digit(10) == expected

def test_render_multi_digit_100():
    # Expected output for number 100:
    # First digit (1):
    # ...
    # ..|
    # ..|
    # Second digit (0):
    # ._.
    # |.|
    # |_|
    # Third digit (0):
    # ._.
    # |.|
    # |_|
    # corresponds to:
    # ...._.._.
    # ..||.||.|
    # ..||_||_|
    expected = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_digit(100) == expected