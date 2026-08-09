from solution import render_digit, render_number

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
    # Line 1: '...' + '._.' = '...._.'
    # Line 2: '..|' + '|.|' = '..||.|'
    # Line 3: '..|' + '|_|' = '..||_|'
    expected = "...._.\n..||.|\n..||_|\n"
    assert render_number(10) == expected

def test_render_multi_digit_100():
    # Expected output for number 100:
    # Line 1: '...' + '._.' + '._.' = '...._.._.'
    # Line 2: '..|' + '|.|' + '|.|' = '..||.||.|'
    # Line 3: '..|' + '|_|' + '|_|' = '..||_||_|'
    expected = "...._.._.\n..||.||.|"\n..||_||_|\n"
    assert render_number(100) == expected