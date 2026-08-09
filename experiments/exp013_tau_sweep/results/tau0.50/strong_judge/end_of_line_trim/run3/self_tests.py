from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    assert trailing_whitespace_cleaner("Hello World!   \n") == "Hello World!\n"  # AC-1.1

def test_remove_trailing_tab():
    assert trailing_whitespace_cleaner("Hello World!\t\t\n") == "Hello World!\n"  # AC-1.2

def test_remove_mixed_trailing_whitespace():
    assert trailing_whitespace_cleaner("Hello World!   \t\n") == "Hello World!\n"  # AC-1.3

def test_trim_final_line():
    assert trailing_whitespace_cleaner("Hello World!   \nThis is a test.   ") == "Hello World!\nThis is a test."  # AC-1.4

def test_preserve_non_whitespace_at_end():
    assert trailing_whitespace_cleaner("Hello World!@   \n") == "Hello World!@\n"  # AC-1.5

def test_no_trailing_whitespace():
    assert trailing_whitespace_cleaner("No trailing whitespace\n") == "No trailing whitespace\n"  # AC-2.1

def test_preserve_leading_whitespace():
    assert trailing_whitespace_cleaner("\tfirst\n \tsecond\r\n") == "\tfirst\n \tsecond\r\n"  # AC-2.2

def test_preserve_inner_whitespace():
    assert trailing_whitespace_cleaner("Inner  spacing\n") == "Inner  spacing\n"  # AC-2.3

def test_empty_text():
    assert trailing_whitespace_cleaner("") == ""  # AC-2.4

def test_unix_line_ending():
    assert trailing_whitespace_cleaner("Line 1\nLine 2\n") == "Line 1\nLine 2\n"  # AC-3.1

def test_windows_line_ending():
    assert trailing_whitespace_cleaner("first \t\r\n") == "first\r\n"  # AC-3.2

def test_mixed_line_endings():
    assert trailing_whitespace_cleaner("one \t\n two \t\r\nthree  ") == "one\n two\r\nthree"  # AC-3.3

def test_whitespace_line_ending():
    assert trailing_whitespace_cleaner(" \t \r\n") == "\r\n"  # AC-3.4

def test_only_line_ending():
    assert trailing_whitespace_cleaner("\n") == "\n"  # AC-3.5

def test_lone_carriage_return():
    assert trailing_whitespace_cleaner("Text with carriage return\r") == "Text with carriage return\r"  # AC-4.1

def test_carriage_return_with_trailing_whitespace():
    assert trailing_whitespace_cleaner("a \r\t \n") == "a \r\n"  # AC-4.2

def test_carriage_return_before_windows_ending():
    assert trailing_whitespace_cleaner("a\r\r\n") == "a\r\r\n"  # AC-4.3

def test_preserve_non_space_whitespace():
    assert trailing_whitespace_cleaner("x\v \n") == "x\v\n"  # Additional test for non-space/non-tab whitespace