from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    input_text = "Hello World    \n"
    expected_output = "Hello World\n"  # Remove trailing spaces
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_trailing_tab():
    input_text = "Hello World\t\n"
    expected_output = "Hello World\n"  # Remove trailing tab
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_mixed_trailing_whitespace():
    input_text = "Hello World    \t\n"
    expected_output = "Hello World\n"  # Remove trailing spaces and tabs
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_trim_final_line():
    input_text = "First line\nSecond line    "
    expected_output = "First line\nSecond line"  # Trim final line spaces
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_only_trailing_whitespace():
    input_text = "Hello World!    \n"
    expected_output = "Hello World!\n"  # Only trailing spaces removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_text_without_trailing_whitespace():
    input_text = "Hello World!\n"
    expected_output = "Hello World!\n"  # No trailing whitespace, unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_leading_whitespace():
    input_text = "    Leading whitespace\n"
    expected_output = "    Leading whitespace\n"  # Leading whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_inner_whitespace():
    input_text = "Hello    World\n"
    expected_output = "Hello    World\n"  # Inner whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_empty_text():
    input_text = ""
    expected_output = ""  # Empty text remains empty
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_keep_unix_line_ending():
    input_text = "Line one\nLine two    \n"
    expected_output = "Line one\nLine two\n"  # Preserve Unix line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_keep_windows_line_ending():
    input_text = "Line one\r\nLine two    \r\n"
    expected_output = "Line one\r\nLine two\r\n"  # Preserve Windows line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_mixed_line_endings():
    input_text = "Line one\nLine two\r\nLine three    \n"
    expected_output = "Line one\nLine two\r\nLine three\n"  # Preserve mixed endings
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_only_line_unix():
    input_text = " \t\n"
    expected_output = "\n"  # Whitespace line keeps just line ending for Unix
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_only_line_windows():
    input_text = " \r\n"
    expected_output = "\r\n"  # Whitespace line keeps just line ending for Windows
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_text_with_only_line_ending():
    input_text = "\n"
    expected_output = "\n"  # Text with only line ending remains unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_text_with_only_windows_line_ending():
    input_text = "\r\n"
    expected_output = "\r\n"  # Text with only Windows line ending remains unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_content_carriage_return():
    input_text = "Line one\rLine two\n"
    expected_output = "Line one\rLine two\n"  # Preserve carriage return as content
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_carriage_return_with_trailing_space():
    input_text = "Line one \rLine two    \n"
    expected_output = "Line one \rLine two\n"  # Preserve content carriage return, remove trailing space
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_carriage_return_before_windows_line_ending():
    input_text = "Hello\r\n"
    expected_output = "Hello\r\n"  # Preserve carriage return before Windows line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_terminal_lone_carriage_return():
    input_text = "value \r"
    expected_output = "value \r"  # Lone carriage return with content before it is preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_content_carriage_return_before_windows_ending():
    input_text = "a\r\r\n"
    expected_output = "a\r\r\n"  # Content carriage return before Windows line ending preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_carriage_return_with_trailing_tab():
    input_text = "a\rb\t\n"
    expected_output = "a\rb\n"  # Preserve content carriage return, remove trailing tab
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_multi_line_trimming():
    input_text = "a \n\tb\t\nc  "
    expected_output = "a\n\tb\nc"  # Trim trailing whitespace from multiple lines
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_space_tab_whitespace():
    input_text = "x\v \n"
    expected_output = "x\v\n"  # Preserve vertical tab, remove trailing space
    assert trailing_whitespace_cleaner(input_text) == expected_output

    input_text = "x\f\t\r\n"
    expected_output = "x\f\r\n"  # Preserve form feed, remove trailing tab
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_crlf_leading_whitespace():
    input_text = " \tindented  \r\n"
    expected_output = " \tindented\r\n"  # Preserve leading whitespace for CRLF
    assert trailing_whitespace_cleaner(input_text) == expected_output