from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    # Input: "Hello World    \n" -> Expected: "Hello World\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Hello World    \n") == "Hello World\n"

def test_remove_trailing_tab():
    # Input: "Hello World\t\t\n" -> Expected: "Hello World\n" (trailing tabs removed)
    assert trailing_whitespace_cleaner("Hello World\t\t\n") == "Hello World\n"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello World    \t\t\n" -> Expected: "Hello World\n" (trailing spaces and tabs removed)
    assert trailing_whitespace_cleaner("Hello World    \t\t\n") == "Hello World\n"

def test_trim_final_line_with_no_line_ending():
    # Input: "Hello World    " -> Expected: "Hello World" (trailing spaces removed, no line ending)
    assert trailing_whitespace_cleaner("Hello World    ") == "Hello World"

def test_preserve_non_whitespace_characters():
    # Input: "Hello World!\t\n" -> Expected: "Hello World!\n" (non-whitespace character preserved)
    assert trailing_whitespace_cleaner("Hello World!\t\n") == "Hello World!\n"

def test_return_unchanged_text_without_trailing_whitespace():
    # Input: "Hello World\n" -> Expected: "Hello World\n" (no trailing whitespace to remove)
    assert trailing_whitespace_cleaner("Hello World\n") == "Hello World\n"

def test_preserve_leading_whitespace():
    # Input: "   Hello World\n" -> Expected: "   Hello World\n" (leading whitespace preserved)
    assert trailing_whitespace_cleaner("   Hello World\n") == "   Hello World\n"

def test_preserve_inner_whitespace():
    # Input: "Hello   World\n" -> Expected: "Hello   World\n" (inner whitespace preserved)
    assert trailing_whitespace_cleaner("Hello   World\n") == "Hello   World\n"

def test_trim_empty_text():
    # Input: "" -> Expected: "" (empty text remains empty)
    assert trailing_whitespace_cleaner("") == ""

def test_preserve_unix_line_ending():
    # Input: "Line 1\nLine 2\n" -> Expected: "Line 1\nLine 2\n" (unix endings preserved)
    assert trailing_whitespace_cleaner("Line 1\nLine 2\n") == "Line 1\nLine 2\n"

def test_preserve_windows_line_ending():
    # Input: "Line 1\r\nLine 2\r\n" -> Expected: "Line 1\r\nLine 2\r\n" (windows endings preserved)
    assert trailing_whitespace_cleaner("Line 1\r\nLine 2\r\n") == "Line 1\r\nLine 2\r\n"

def test_mixed_line_endings():
    # Input: "Line 1\nLine 2\r\n" -> Expected: "Line 1\nLine 2\r\n" (mixed endings preserved)
    assert trailing_whitespace_cleaner("Line 1\nLine 2\r\n") == "Line 1\nLine 2\r\n"

def test_whitespace_only_line_keeps_its_ending():
    # Input: "   \n" -> Expected: "   \n" (whitespace only keeps line ending)
    assert trailing_whitespace_cleaner("   \n") == "   \n"

def test_only_line_ending_is_returned():
    # Input: "\n" -> Expected: "\n" (only a line ending is returned unchanged)
    assert trailing_whitespace_cleaner("\n") == "\n"

def test_only_windows_line_ending_is_returned():
    # Input: "\r\n" -> Expected: "\r\n" (only a windows line ending is returned unchanged)
    assert trailing_whitespace_cleaner("\r\n") == "\r\n"

def test_lone_carriage_return_is_content():
    # Input: "Hello\rWorld\n" -> Expected: "Hello\rWorld\n" (carriage return treated as content)
    assert trailing_whitespace_cleaner("Hello\rWorld\n") == "Hello\rWorld\n"

def test_preserve_whitespace_before_lone_carriage_return():
    # Input: "Hello  \r World\n" -> Expected: "Hello  \r World\n" (whitespace before carriage return preserved)
    assert trailing_whitespace_cleaner("Hello  \r World\n") == "Hello  \r World\n"

def test_remove_trailing_whitespace_before_lone_carriage_return():
    # Input: "Hello   \r World  \n" -> Expected: "Hello   \r World\n" (trailing whitespace removed)
    assert trailing_whitespace_cleaner("Hello   \r World  \n") == "Hello   \r World\n"

def test_carriage_return_before_windows_line_ending():
    # Input: "Hello\r\r\n" -> Expected: "Hello\r\r\n" (carriage return before windows ending preserved)
    assert trailing_whitespace_cleaner("Hello\r\r\n") == "Hello\r\r\n"