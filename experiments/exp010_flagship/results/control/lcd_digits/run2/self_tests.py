from solution import render_digit, render_number

def test_render_single_digit_0():
    # Expected output for digit 0:
    # ._.
    # |.|
    # |_|
    expected = ".\n_\n.\n|\n|\n_\n"
    assert render_digit(0) == expected

def test_render_single_digit_1():
    # Expected output for digit 1:
    # ...
    # ..|
    # ..|
    expected = "...\n..|\n..|\n"
    assert render_digit(1) == expected

def test_render_single_digit_2():
    # Expected output for digit 2:
    # ._.
    # ..|
    # |_|
    expected = ".\n_\n|\n.\n|\n_\n"
    assert render_digit(2) == expected

def test_render_single_digit_3():
    # Expected output for digit 3:
    # ._.
    # ..|
    # ._|
    expected = ".\n_\n|\n.\n|\n_\n"
    assert render_digit(3) == expected

def test_render_single_digit_4():
    # Expected output for digit 4:
    # ...
    # |.|
    # ..|
    expected = "...\n|.|\n..|\n"
    assert render_digit(4) == expected

def test_render_single_digit_5():
    # Expected output for digit 5:
    # ._.
    # |..
    # ._|
    expected = ".\n_\n|\n|.\n|\n_\n"
    assert render_digit(5) == expected

def test_render_single_digit_6():
    # Expected output for digit 6:
    # ._.
    # |.|
    # ._|
    expected = ".\n_\n|\n|.|\n|\n_\n"
    assert render_digit(6) == expected

def test_render_single_digit_7():
    # Expected output for digit 7:
    # ._.
    # ..|
    # ..|
    expected = ".\n_\n..\n..|\n..|\n"
    assert render_digit(7) == expected

def test_render_single_digit_8():
    # Expected output for digit 8:
    # ._.
    # |.|
    # ._|
    expected = ".\n_\n|\n|.|\n|\n_\n"
    assert render_digit(8) == expected

def test_render_single_digit_9():
    # Expected output for digit 9:
    # ._.
    # |.|
    # ._|
    expected = ".\n_\n|\n|.|\n|\n_\n"
    assert render_digit(9) == expected

def test_render_multi_digit_10():
    # Expected output for number 10:
    # ...._.
    # ..||.|
    # ..||_|
    expected = "....\n._.\n..|\n..|\n"
    assert render_number(10) == expected

def test_render_multi_digit_100():
    # Expected output for number 100:
    # ...._.._.
    # ..||.||.|
    # ..||_||_|
    expected = "....\n._.._.\n..||\n..||\n"
    assert render_number(100) == expected

def test_render_empty_input():
    # Expected output for empty input:
    # (nothing should be rendered)
    expected = ""
    assert render_number("") == expected