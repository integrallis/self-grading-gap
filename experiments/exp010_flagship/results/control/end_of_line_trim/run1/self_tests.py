from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    # Input: "Hello World!   \n"
    # Expected: "Hello World!\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Hello World!   \n") == "Hello World!\n"

def test_remove_trailing_tab():
    # Input: "Hello World!\t\n"
    # Expected: "Hello World!\n" (trailing tab removed)
    assert trailing_whitespace_cleaner("Hello World!\t\n") == "Hello World!\n"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello World!   \t\n"
    # Expected: "Hello World!\n" (trailing spaces and tab removed)
    assert trailing_whitespace_cleaner("Hello World!   \t\n") == "Hello World!\n"

def test_trim_final_line_with_no_line_ending():
    # Input: "Hello World!   "
    # Expected: "Hello World!" (trailing spaces removed, no line ending)
    assert trailing_whitespace_cleaner("Hello World!   ") == "Hello World!"

def test_remove_trailing_whitespace_only():
    # Input: "Line with only whitespace    \n"
    # Expected: "Line with only whitespace\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Line with only whitespace    \n") == "Line with only whitespace\n"

def test_preserve_text_without_trailing_whitespace():
    # Input: "No trailing whitespace here.\n"
    # Expected: "No trailing whitespace here.\n" (unchanged)
    assert trailing_whitespace_cleaner("No trailing whitespace here.\n") == "No trailing whitespace here.\n"

def test_preserve_leading_whitespace():
    # Input: "    Leading spaces\n"
    # Expected: "    Leading spaces\n" (leading spaces preserved)
    assert trailing_whitespace_cleaner("    Leading spaces\n") == "    Leading spaces\n"

def test_preserve_inner_whitespace():
    # Input: "Inner   spaces   preserved\n"
    # Expected: "Inner   spaces   preserved\n" (inner spaces preserved)
    assert trailing_whitespace_cleaner("Inner   spaces   preserved\n") == "Inner   spaces   preserved\n"

def test_empty_text():
    # Input: ""
    # Expected: "" (empty text remains empty)
    assert trailing_whitespace_cleaner("") == ""

def test_keep_unix_line_ending():
    # Input: "Line one\nLine two\n"
    # Expected: "Line one\nLine two\n" (Unix line endings preserved)
    assert trailing_whitespace_cleaner("Line one\nLine two\n") == "Line one\nLine two\n"

def test_keep_windows_line_ending():
    # Input: "Line one\r\nLine two\r\n"
    # Expected: "Line one\r\nLine two\r\n" (Windows line endings preserved)
    assert trailing_whitespace_cleaner("Line one\r\nLine two\r\n") == "Line one\r\nLine two\r\n"

def test_mixed_line_endings():
    # Input: "Line one\nLine two\r\nLine three\n"
    # Expected: "Line one\nLine two\r\nLine three\n" (mixed line endings preserved)
    assert trailing_whitespace_cleaner("Line one\nLine two\r\nLine three\n") == "Line one\nLine two\r\nLine three\n"

def test_whitespace_line_with_line_ending():
    # Input: "      \n"
    # Expected: "\n" (whitespace line keeps line ending)
    assert trailing_whitespace_cleaner("      \n") == "\n"

def test_only_line_ending():
    # Input: "\n"
    # Expected: "\n" (only line ending remains unchanged)
    assert trailing_whitespace_cleaner("\n") == "\n"

def test_only_windows_line_ending():
    # Input: "\r\n"
    # Expected: "\r\n" (only Windows line ending remains unchanged)
    assert trailing_whitespace_cleaner("\r\n") == "\r\n"

def test_content_carriage_return():
    # Input: "Text with carriage return\rText continues\n"
    # Expected: "Text with carriage return\rText continues\n" (carriage return treated as content)
    assert trailing_whitespace_cleaner("Text with carriage return\rText continues\n") == "Text with carriage return\rText continues\n"

def test_trailing_spaces_before_carriage_return():
    # Input: "Text with spaces before carriage return    \rText continues\n"
    # Expected: "Text with spaces before carriage return\rText continues\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Text with spaces before carriage return    \rText continues\n") == "Text with spaces before carriage return\rText continues\n"

def test_carriage_return_before_windows_line_ending():
    # Input: "Text before\rText continues\r\n"
    # Expected: "Text before\rText continues\r\n" (carriage return before Windows line ending preserved)
    assert trailing_whitespace_cleaner("Text before\rText continues\r\n") == "Text before\rText continues\r\n"