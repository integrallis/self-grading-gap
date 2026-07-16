from solution import *

def test_render_single_digit_0():
    # Expected output for digit 0
    expected_output = "._.\n|.|\n|_|\n"
    assert render_number(0) == expected_output

def test_render_single_digit_1():
    # Expected output for digit 1
    expected_output = "...\n..|\n..|\n"
    assert render_number(1) == expected_output

def test_render_multi_digit_10():
    # Expected output for number 10
    # 1 -> 
    # .  ._.
    # .  |.|
    # .  |_|
    
    expected_output = "...._.\n..||.|\n..||_|\n"
    assert render_number(10) == expected_output

def test_render_multi_digit_100():
    # Expected output for number 100
    # 1 -> 
    # .  ._.._.
    # .  |.||.|
    # .  |_||_|

    expected_output = "...._.._.\n..||.||.|\n..||_||_|\n"
    assert render_number(100) == expected_output

def test_render_multi_digit_101():
    # Expected output for number 101
    # 1 -> 
    # .  ._.
    # .  |.|
    # .  |_|
    
    # 0 -> 
    # ._.
    # |.|
    # |_|
    
    expected_output = "...._....\n..||.|..|\n..||_|..|\n"
    assert render_number(101) == expected_output