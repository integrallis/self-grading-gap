from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    input_text = "Hello World    \n"
    expected_output = "Hello World\n"  # Trailing spaces removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_trailing_tab():
    input_text = "Hello World\t\t\n"
    expected_output = "Hello World\n"  # Trailing tabs removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_mixed_trailing_whitespace():
    input_text = "Hello World    \t\n"
    expected_output = "Hello World\n"  # Mixed trailing spaces and tabs removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_trim_final_line():
    input_text = "Line 1   \nLine 2\t"  # Final line without line ending
    expected_output = "Line 1\nLine 2"  # Final line trimmed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_only_trailing_whitespace_removed():
    input_text = "Text with a space at the end    \n"
    expected_output = "Text with a space at the end\n"  # Only trailing spaces removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_trailing_whitespace():
    input_text = "    Leading spaces\n\tLeading tabs\n"
    expected_output = "    Leading spaces\n\tLeading tabs\n"  # Non-trailing whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_inner_whitespace():
    input_text = "Text with   multiple   spaces\n"
    expected_output = "Text with   multiple   spaces\n"  # Inner whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_empty_text():
    input_text = ""
    expected_output = ""  # Empty text remains empty
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_unix_line_endings():
    input_text = "Line 1\nLine 2   \n"
    expected_output = "Line 1\nLine 2\n"  # Unix line endings preserved, trailing whitespace removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_windows_line_endings():
    input_text = "Line 1\r\nLine 2   \r\n"
    expected_output = "Line 1\r\nLine 2\r\n"  # Windows line endings preserved, trailing whitespace removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_mixed_line_endings():
    input_text = "Line 1\r\nLine 2\nLine 3   \r\n"
    expected_output = "Line 1\r\nLine 2\nLine 3\r\n"  # Mixed line endings preserved, trailing whitespace removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_line():
    input_text = "    \n"
    expected_output = "\n"  # Line of whitespace keeps just its line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_only_line_ending():
    input_text = "\n"
    expected_output = "\n"  # Text that is just a line ending remains unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_only_windows_line_ending():
    input_text = "\r\n"
    expected_output = "\r\n"  # Text that is just a Windows line ending remains unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_lone_carriage_return_as_content():
    input_text = "Line 1\rContent\r\n"
    expected_output = "Line 1\rContent\r\n"  # Carriage return treated as content, not line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_whitespace_before_lone_carriage_return():
    input_text = "Line 1    \r    \n"
    expected_output = "Line 1    \r\n"  # Trailing spaces before lone carriage return removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_carriage_return_before_windows_line_ending():
    input_text = "Text\r\r\n"
    expected_output = "Text\r\r\n"  # Carriage return preserved before Windows line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_space_tab_whitespace():
    input_text = "a\v \n"  # Vertical tab is preserved
    expected_output = "a\v\n"  # Non-space/tab whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_space_tab_whitespace_windows():
    input_text = "a\f\r\n"  # Form feed is preserved
    expected_output = "a\f\r\n"  # Non-space/tab whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_lone_carriage_return_final_character():
    input_text = "a \r"  # Lone carriage return as final character
    expected_output = "a \r"  # Content preserved, trailing space removed
    assert trailing_whitespace_cleaner(input_text) == expected_output