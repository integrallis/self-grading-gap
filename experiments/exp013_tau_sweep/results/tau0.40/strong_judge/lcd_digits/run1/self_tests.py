from solution import render_lcd_digit

def test_render_single_digit_0():
    # Expected output for digit 0:
    expected_output = "._.\n|.|\n|_|\n"
    assert render_lcd_digit(0) == expected_output

def test_render_single_digit_1():
    # Expected output for digit 1:
    expected_output = "...\n..|\n..|\n"
    assert render_lcd_digit(1) == expected_output

def test_render_multi_digit_10():
    # Expected output for number 10:
    expected_output = "...._.\n..||.|\n..||_|\n"
    assert render_lcd_digit(10) == expected_output

def test_render_multi_digit_100():
    # Expected output for number 100:
    expected_output = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_lcd_digit(100) == expected_output

def test_render_single_digit_output_lines():
    # Ensure that the output has exactly three lines for a single digit
    output = render_lcd_digit(0)
    assert output.count('\n') == 3
    assert output.endswith('\n')

def test_render_multi_digit_output_lines():
    # Ensure that the output has exactly three lines for multi-digit numbers
    output = render_lcd_digit(10)
    assert output.count('\n') == 3
    assert output.endswith('\n')
    output = render_lcd_digit(100)
    assert output.count('\n') == 3
    assert output.endswith('\n')