from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    # Input: "Hello, World!   \n"
    # Expected: "Hello, World!\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Hello, World!   \n") == "Hello, World!\n"

def test_remove_trailing_tab():
    # Input: "Hello, World!\t\n"
    # Expected: "Hello, World!\n" (trailing tab removed)
    assert trailing_whitespace_cleaner("Hello, World!\t\n") == "Hello, World!\n"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello, World!   \t\n"
    # Expected: "Hello, World!\n" (trailing spaces and tabs removed)
    assert trailing_whitespace_cleaner("Hello, World!   \t\n") == "Hello, World!\n"

def test_trim_final_line_without_line_ending():
    # Input: "Hello, World!   "
    # Expected: "Hello, World!" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Hello, World!   ") == "Hello, World!"

def test_preserve_non_whitespace_characters():
    # Input: "Hello, World!xyz   \n"
    # Expected: "Hello, World!xyz\n" (no trailing whitespace removed)
    assert trailing_whitespace_cleaner("Hello, World!xyz   \n") == "Hello, World!xyz\n"

def test_preserve_leading_whitespace():
    # Input: "   Hello, World!   \n"
    # Expected: "   Hello, World!\n" (leading spaces preserved)
    assert trailing_whitespace_cleaner("   Hello, World!   \n") == "   Hello, World!\n"

def test_preserve_inner_whitespace():
    # Input: "Hello,   World!\n"
    # Expected: "Hello,   World!\n" (inner spaces preserved)
    assert trailing_whitespace_cleaner("Hello,   World!\n") == "Hello,   World!\n"

def test_empty_text():
    # Input: ""
    # Expected: "" (empty input returns empty)
    assert trailing_whitespace_cleaner("") == ""

def test_keep_unix_line_ending():
    # Input: "Line 1\nLine 2   \n"
    # Expected: "Line 1\nLine 2\n" (trailing spaces removed, Unix line ending preserved)
    assert trailing_whitespace_cleaner("Line 1\nLine 2   \n") == "Line 1\nLine 2\n"

def test_keep_windows_line_ending():
    # Input: "Line 1\r\nLine 2   \r\n"
    # Expected: "Line 1\r\nLine 2\r\n" (trailing spaces removed, Windows line ending preserved)
    assert trailing_whitespace_cleaner("Line 1\r\nLine 2   \r\n") == "Line 1\r\nLine 2\r\n"

def test_mixed_line_endings():
    # Input: "Line 1\nLine 2   \r\n"
    # Expected: "Line 1\nLine 2\r\n" (trailing spaces removed, mixed line endings preserved)
    assert trailing_whitespace_cleaner("Line 1\nLine 2   \r\n") == "Line 1\nLine 2\r\n"

def test_whitespace_only_line():
    # Input: "   \r\n"
    # Expected: "\r\n" (whitespace only line keeps line ending)
    assert trailing_whitespace_cleaner("   \r\n") == "\r\n"

def test_only_line_ending():
    # Input: "\n"
    # Expected: "\n" (only a line ending returns unchanged)
    assert trailing_whitespace_cleaner("\n") == "\n"

def test_only_windows_line_ending():
    # Input: "\r\n"
    # Expected: "\r\n" (only a Windows line ending returns unchanged)
    assert trailing_whitespace_cleaner("\r\n") == "\r\n"

def test_lone_carriage_return_content():
    # Input: "Hello, World!\r"
    # Expected: "Hello, World!\r" (lone carriage return is treated as content)
    assert trailing_whitespace_cleaner("Hello, World!\r") == "Hello, World!\r"

def test_carriage_return_with_trailing_space():
    # Input: "Hello, World!  \r   \n"
    # Expected: "Hello, World!  \r\n" (trailing spaces removed, carriage return preserved)
    assert trailing_whitespace_cleaner("Hello, World!  \r   \n") == "Hello, World!  \r\n"

def test_carriage_return_before_windows_line_ending():
    # Input: "Hello\r \r\n"
    # Expected: "Hello\r\r\n" (trailing space removed, carriage return preserved)
    assert trailing_whitespace_cleaner("Hello\r \r\n") == "Hello\r\r\n"

def test_carriage_return_does_not_split_line():
    # Input: "a \rb\n"
    # Expected: "a \rb\n" (lone carriage return does not split the line)
    assert trailing_whitespace_cleaner("a \rb\n") == "a \rb\n"

def test_survive_non_space_tab_trailing_character_unix():
    # Input: "\v\n"
    # Expected: "\v\n" (non-space/tab character before Unix end survives)
    assert trailing_whitespace_cleaner("\v\n") == "\v\n"

def test_survive_non_space_tab_trailing_character_windows():
    # Input: "\v\r\n"
    # Expected: "\v\r\n" (non-space/tab character before Windows end survives)
    assert trailing_whitespace_cleaner("\v\r\n") == "\v\r\n"

def test_preserve_leading_indentation():
    # Input: "\t    Line 1\n\t    Line 2   \n"
    # Expected: "\t    Line 1\n\t    Line 2\n" (leading tabs and spaces preserved)
    assert trailing_whitespace_cleaner("\t    Line 1\n\t    Line 2   \n") == "\t    Line 1\n\t    Line 2\n"

def test_trim_non_final_line_with_trailing_whitespace():
    # Input: "first \t\nlast"
    # Expected: "first\nlast" (trailing whitespace removed from non-final line)
    assert trailing_whitespace_cleaner("first \t\nlast") == "first\nlast"

def test_carriage_return_before_windows_line_ending_adjacency():
    # Input: "a\r\r\n"
    # Expected: "a\r\r\n" (content carriage return before Windows line ending)
    assert trailing_whitespace_cleaner("a\r\r\n") == "a\r\r\n"