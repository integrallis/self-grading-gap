from solution import render_number

def test_render_single_digit_0():
    # Expected output for digit 0
    expected = ".\n_\n.\n|.|\n|_|\n"
    assert render_number(0) == expected

def test_render_single_digit_1():
    # Expected output for digit 1
    expected = ".\n.\n.\n..|\n..|\n"
    assert render_number(1) == expected

def test_render_single_digit_2():
    # Expected output for digit 2
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(2) == expected

def test_render_single_digit_3():
    # Expected output for digit 3
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(3) == expected

def test_render_single_digit_4():
    # Expected output for digit 4
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(4) == expected

def test_render_single_digit_5():
    # Expected output for digit 5
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(5) == expected

def test_render_single_digit_6():
    # Expected output for digit 6
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(6) == expected

def test_render_single_digit_7():
    # Expected output for digit 7
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(7) == expected

def test_render_single_digit_8():
    # Expected output for digit 8
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(8) == expected

def test_render_single_digit_9():
    # Expected output for digit 9
    expected = ".\n.\n.\n|.|\n|_|\n"
    assert render_number(9) == expected

def test_render_multi_digit_10():
    # Expected output for number 10
    expected = "...._.\n..||.|\n..||_|\n"
    assert render_number(10) == expected

def test_render_multi_digit_100():
    # Expected output for number 100
    expected = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_number(100) == expected

def test_render_single_digit_0_as_number():
    # Expected output for number 0 as a standalone
    expected = ".\n_\n.\n|.|\n|_|\n"
    assert render_number(0) == expected