from solution import trailing_whitespace_cleaner

def test_remove_trailing_space():
    # Input: "Hello World!    \n"
    # Expected: "Hello World!\n" (trailing spaces removed)
    assert trailing_whitespace_cleaner("Hello World!    \n") == "Hello World!\n"

def test_remove_trailing_tab():
    # Input: "Hello World!\t\n"
    # Expected: "Hello World!\n" (trailing tab removed)
    assert trailing_whitespace_cleaner("Hello World!\t\n") == "Hello World!\n"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello World!    \t\n"
    # Expected: "Hello World!\n" (trailing spaces and tab removed)
    assert trailing_whitespace_cleaner("Hello World!    \t\n") == "Hello World!\n"

def test_trim_final_line():
    # Input: "first  \nlast \t "
    # Expected: "first\nlast" (trailing spaces removed from the final line)
    assert trailing_whitespace_cleaner("first  \nlast \t ") == "first\nlast"

def test_trim_empty_line():
    # Input: "Hello World!\n\n"
    # Expected: "Hello World!\n\n" (empty line remains)
    assert trailing_whitespace_cleaner("Hello World!\n\n") == "Hello World!\n\n"

def test_no_trailing_whitespace():
    # Input: "Hello World!\nGoodbye!\n"
    # Expected: "Hello World!\nGoodbye!\n" (no trailing whitespace)
    assert trailing_whitespace_cleaner("Hello World!\nGoodbye!\n") == "Hello World!\nGoodbye!\n"

def test_preserve_leading_whitespace():
    # Input: "    Hello World!\n"
    # Expected: "    Hello World!\n" (leading spaces preserved)
    assert trailing_whitespace_cleaner("    Hello World!\n") == "    Hello World!\n"

def test_preserve_leading_tabs():
    # Input: "\t  text\t \r\n"
    # Expected: "\t  text\r\n" (leading tabs preserved, trailing whitespace removed)
    assert trailing_whitespace_cleaner("\t  text\t \r\n") == "\t  text\r\n"

def test_preserve_internal_whitespace():
    # Input: "Hello    World!\n"
    # Expected: "Hello    World!\n" (internal spaces preserved)
    assert trailing_whitespace_cleaner("Hello    World!\n") == "Hello    World!\n"

def test_preserve_internal_tabs():
    # Input: "left\t\tright\n"
    # Expected: "left\t\tright\n" (internal tabs preserved)
    assert trailing_whitespace_cleaner("left\t\tright\n") == "left\t\tright\n"

def test_empty_text():
    # Input: ""
    # Expected: "" (empty text remains empty)
    assert trailing_whitespace_cleaner("") == ""

def test_unix_line_ending():
    # Input: "Hello World!    \nGoodbye!    \n"
    # Expected: "Hello World!\nGoodbye!\n" (trailing whitespace removed, Unix line endings preserved)
    assert trailing_whitespace_cleaner("Hello World!    \nGoodbye!    \n") == "Hello World!\nGoodbye!\n"

def test_windows_line_ending():
    # Input: "Hello World!    \r\nGoodbye!    \r\n"
    # Expected: "Hello World!\r\nGoodbye!\r\n" (trailing whitespace removed, Windows line endings preserved)
    assert trailing_whitespace_cleaner("Hello World!    \r\nGoodbye!    \r\n") == "Hello World!\r\nGoodbye!\r\n"

def test_mixed_line_endings():
    # Input: "Hello World!    \nGoodbye!    \r\n"
    # Expected: "Hello World!\nGoodbye!\r\n" (trailing whitespace removed, mixed line endings preserved)
    assert trailing_whitespace_cleaner("Hello World!    \nGoodbye!    \r\n") == "Hello World!\nGoodbye!\r\n"

def test_line_with_only_whitespace():
    # Input: "\t \r\n"
    # Expected: "\r\n" (only whitespace line keeps its line ending)
    assert trailing_whitespace_cleaner("\t \r\n") == "\r\n"

def test_only_carriage_return():
    # Input: "\r"
    # Expected: "\r" (lone carriage return treated as content)
    assert trailing_whitespace_cleaner("\r") == "\r"

def test_carriage_return_before_line_ending():
    # Input: "Hello\r\n"
    # Expected: "Hello\r\n" (carriage return is part of the Windows line ending)
    assert trailing_whitespace_cleaner("Hello\r\n") == "Hello\r\n"

def test_preserve_content_carriage_return():
    # Input: "Hello\r\r\n"
    # Expected: "Hello\r\r\n" (first carriage return is content, second is line ending)
    assert trailing_whitespace_cleaner("Hello\r\r\n") == "Hello\r\r\n"

def test_preserve_trailing_spaces_before_carriage_return():
    # Input: "Hello    \r"
    # Expected: "Hello    \r" (spaces before carriage return are interior, not trailing)
    assert trailing_whitespace_cleaner("Hello    \r") == "Hello    \r"

def test_space_after_content_carriage_return():
    # Input: "Hello\r    \n"
    # Expected: "Hello\r\n" (spaces after carriage return are trailing and removed)
    assert trailing_whitespace_cleaner("Hello\r    \n") == "Hello\r\n"

def test_space_after_content_tab_carriage_return():
    # Input: "a\r\t \r\n"
    # Expected: "a\r\r\n" (spaces after content carriage return are trimmed)
    assert trailing_whitespace_cleaner("a\r\t \r\n") == "a\r\r\n"

def test_whitespace_only_tab_line():
    # Input: "\t \r\n"
    # Expected: "\r\n" (only whitespace line keeps its line ending)
    assert trailing_whitespace_cleaner("\t \r\n") == "\r\n"

def test_unix_line_ending_only():
    # Input: "\n"
    # Expected: "\n" (text consisting solely of a Unix line ending is unchanged)
    assert trailing_whitespace_cleaner("\n") == "\n"

def test_windows_line_ending_only():
    # Input: "\r\n"
    # Expected: "\r\n" (text consisting solely of a Windows line ending is unchanged)
    assert trailing_whitespace_cleaner("\r\n") == "\r\n"