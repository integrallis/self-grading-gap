from solution import render_digits

def test_render_digit_0():
    # Expected output for digit 0:
    # ._.
    # |.|
    # |_|
    expected_output = "._.\n|.|\n|_|\n"
    assert render_digits(0) == expected_output

def test_render_digit_1():
    # Expected output for digit 1:
    # ...
    # ..|
    # ..|
    expected_output = "...\n..|\n..|\n"
    assert render_digits(1) == expected_output

def test_render_digit_2():
    # Expected output for digit 2:
    # ._.
    # ._|
    # |_.
    expected_output = "._.\n._|\n|_.\n"
    assert render_digits(2) == expected_output

def test_render_digit_3():
    # Expected output for digit 3:
    # ._.
    # ._|
    # ._|
    expected_output = "._.\n._|\n._|\n"
    assert render_digits(3) == expected_output

def test_render_digit_4():
    # Expected output for digit 4:
    # ...
    # |.|
    # ._|
    expected_output = "...\n|.|\n._|\n"
    assert render_digits(4) == expected_output

def test_render_digit_5():
    # Expected output for digit 5:
    # ._.
    # |._
    # ._|
    expected_output = "._.\n|._\n._|\n"
    assert render_digits(5) == expected_output

def test_render_digit_6():
    # Expected output for digit 6:
    # ._.
    # |._
    # |_|
    expected_output = "._.\n|._\n|_|\n"
    assert render_digits(6) == expected_output

def test_render_digit_7():
    # Expected output for digit 7:
    # ._.
    # ..|
    # ..|
    expected_output = "._.\n..|\n..|\n"
    assert render_digits(7) == expected_output

def test_render_digit_8():
    # Expected output for digit 8:
    # ._.
    # |.|
    # |_|
    expected_output = "._.\n|.|\n|_|\n"
    assert render_digits(8) == expected_output

def test_render_digit_9():
    # Expected output for digit 9:
    # ._.
    # |.|
    # ._|
    expected_output = "._.\n|.|\n._|\n"
    assert render_digits(9) == expected_output

def test_render_multiple_digits_10():
    # Expected output for number 10:
    # ...._.
    # ..||.|
    # ..||_|
    expected_output = "...._.\n..||.|\n..||_|\n"
    assert render_digits(10) == expected_output

def test_render_multiple_digits_100():
    # Expected output for number 100:
    # ...._.._.
    # ..||.||.|
    # ..||_||_|
    expected_output = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_digits(100) == expected_output