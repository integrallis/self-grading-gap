from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    input_text = "Hello, World!   \n"
    expected_output = "Hello, World!\n"  # Trailing spaces removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_trailing_tab():
    input_text = "Hello, World!\t\n"
    expected_output = "Hello, World!\n"  # Trailing tab removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_remove_mixed_trailing_whitespace():
    input_text = "Hello, World!   \t\n"
    expected_output = "Hello, World!\n"  # Mixed trailing spaces and tabs removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_trim_final_line_without_line_ending():
    input_text = "Line 1\nLine 2   "
    expected_output = "Line 1\nLine 2"  # Final line trimmed even without line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_whitespace_characters():
    input_text = "Hello, World!#   \n"
    expected_output = "Hello, World!#\n"  # Non-whitespace character preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_return_unchanged_text_without_trailing_whitespace():
    input_text = "No trailing whitespace here!\n"
    expected_output = "No trailing whitespace here!\n"  # Text unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_leading_whitespace():
    input_text = "    Hello\n\tWorld!\n"
    expected_output = "    Hello\n\tWorld!\n"  # Leading whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_inner_whitespace():
    input_text = "Hello    World!\n"
    expected_output = "Hello    World!\n"  # Inner whitespace untouched
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_empty_text_remains_empty():
    input_text = ""
    expected_output = ""  # Empty text returns empty
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_keep_unix_line_endings():
    input_text = "Line 1\nLine 2   \n"
    expected_output = "Line 1\nLine 2\n"  # Unix line endings preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_keep_windows_line_endings():
    input_text = "Line 1\r\nLine 2   \r\n"
    expected_output = "Line 1\r\nLine 2\r\n"  # Windows line endings preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_mixed_line_endings():
    input_text = "Line 1\nLine 2\r\nLine 3   \n"
    expected_output = "Line 1\nLine 2\r\nLine 3\n"  # Mixed line endings preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_line_keeps_line_ending():
    input_text = "   \n"
    expected_output = "\n"  # Whitespace line keeps line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_only_windows_line_keeps_line_ending():
    input_text = " \t\r\n"
    expected_output = "\r\n"  # Whitespace-only Windows line keeps line ending
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_text_with_only_unix_line_ending():
    input_text = "\n"
    expected_output = "\n"  # Text with only Unix line ending returns unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_text_with_only_line_ending():
    input_text = "\r\n"
    expected_output = "\r\n"  # Text with only line ending returns unchanged
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_lone_carriage_return_as_content():
    input_text = "Hello\rWorld\n"
    expected_output = "Hello\rWorld\n"  # Carriage return not followed by line feed preserved as content
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_whitespace_before_lone_carriage_return():
    input_text = "Hello   \rWorld\n"
    expected_output = "Hello   \rWorld\n"  # Whitespace before carriage return preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_whitespace_after_lone_carriage_return_removed():
    input_text = "Hello   \rWorld \t\r\n"
    expected_output = "Hello   \rWorld\r\n"  # Whitespace after lone carriage return removed
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_content_carriage_return_before_windows_line_ending():
    input_text = "Hello\r\r\n"
    expected_output = "Hello\r\r\n"  # Content carriage return before Windows line ending preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_lone_carriage_return_at_end():
    input_text = "Hello\r"
    expected_output = "Hello\r"  # Lone carriage return at end preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output

def test_preserve_non_space_tab_whitespace():
    input_text = "a\v\nb\f\r\n"
    expected_output = "a\v\nb\f\r\n"  # Non-space/tab whitespace preserved
    assert trailing_whitespace_cleaner(input_text) == expected_output