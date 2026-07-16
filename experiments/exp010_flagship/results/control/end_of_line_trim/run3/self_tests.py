from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    # Input: "Hello World!    " -> expected: "Hello World!"
    assert trailing_whitespace_cleaner("Hello World!    ") == "Hello World!"

def test_remove_trailing_tab():
    # Input: "Hello World!\t\t" -> expected: "Hello World!"
    assert trailing_whitespace_cleaner("Hello World!\t\t") == "Hello World!"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello World!    \t\t" -> expected: "Hello World!"
    assert trailing_whitespace_cleaner("Hello World!    \t\t") == "Hello World!"

def test_trim_final_line_without_line_ending():
    # Input: "Line 1\nLine 2    " -> expected: "Line 1\nLine 2"
    assert trailing_whitespace_cleaner("Line 1\nLine 2    ") == "Line 1\nLine 2"

def test_preserve_non_whitespace_characters():
    # Input: "End of line!xyz" -> expected: "End of line!xyz"
    assert trailing_whitespace_cleaner("End of line!xyz") == "End of line!xyz"

def test_preserve_leading_whitespace():
    # Input: "    Leading spaces" -> expected: "    Leading spaces"
    assert trailing_whitespace_cleaner("    Leading spaces") == "    Leading spaces"

def test_preserve_inner_whitespace():
    # Input: "This is  a test" -> expected: "This is  a test"
    assert trailing_whitespace_cleaner("This is  a test") == "This is  a test"

def test_empty_text():
    # Input: "" -> expected: ""
    assert trailing_whitespace_cleaner("") == ""

def test_keep_unix_line_ending():
    # Input: "Line 1\nLine 2\n" -> expected: "Line 1\nLine 2\n"
    assert trailing_whitespace_cleaner("Line 1\nLine 2\n") == "Line 1\nLine 2\n"

def test_keep_windows_line_ending():
    # Input: "Line 1\r\nLine 2\r\n" -> expected: "Line 1\r\nLine 2\r\n"
    assert trailing_whitespace_cleaner("Line 1\r\nLine 2\r\n") == "Line 1\r\nLine 2\r\n"

def test_mixed_line_endings():
    # Input: "Line 1\nLine 2\r\nLine 3\n" -> expected: "Line 1\nLine 2\r\nLine 3\n"
    assert trailing_whitespace_cleaner("Line 1\nLine 2\r\nLine 3\n") == "Line 1\nLine 2\r\nLine 3\n"

def test_whitespace_only_line():
    # Input: "   \n" -> expected: "\n"
    assert trailing_whitespace_cleaner("   \n") == "\n"

def test_text_with_only_line_ending():
    # Input: "\n" -> expected: "\n"
    assert trailing_whitespace_cleaner("\n") == "\n"

def test_content_carriage_return():
    # Input: "Text with content\rMore text\n" -> expected: "Text with content\rMore text\n"
    assert trailing_whitespace_cleaner("Text with content\rMore text\n") == "Text with content\rMore text\n"

def test_preserve_carriage_return_as_content():
    # Input: "Hello\rWorld\n" -> expected: "Hello\rWorld"
    assert trailing_whitespace_cleaner("Hello\rWorld\n") == "Hello\rWorld"

def test_preserve_whitespace_before_carriage_return():
    # Input: "Before\r  \n" -> expected: "Before\r\n"
    assert trailing_whitespace_cleaner("Before\r  \n") == "Before\r\n"

def test_carriage_return_before_windows_ending():
    # Input: "a\r\r\n" -> expected: "a\r\r\n"
    assert trailing_whitespace_cleaner("a\r\r\n") == "a\r\r\n"