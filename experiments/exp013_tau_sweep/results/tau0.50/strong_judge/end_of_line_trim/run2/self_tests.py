from solution import clean_trailing_whitespace

def test_remove_trailing_spaces():
    # Input: "Hello World    " -> Expected: "Hello World"
    assert clean_trailing_whitespace("Hello World    ") == "Hello World"

def test_remove_trailing_tabs():
    # Input: "Hello World\t\t" -> Expected: "Hello World"
    assert clean_trailing_whitespace("Hello World\t\t") == "Hello World"

def test_remove_mixed_trailing_whitespace():
    # Input: "Hello World    \t\t" -> Expected: "Hello World"
    assert clean_trailing_whitespace("Hello World    \t\t") == "Hello World"

def test_trim_final_line_without_ending():
    # Input: "Hello\nWorld    " -> Expected: "Hello\nWorld"
    assert clean_trailing_whitespace("Hello\nWorld    ") == "Hello\nWorld"

def test_only_spaces_and_tabs_removed():
    # Input: "Hello World!" -> Expected: "Hello World!"
    assert clean_trailing_whitespace("Hello World!") == "Hello World!"

def test_preserve_leading_whitespace():
    # Input: "    Hello World    " -> Expected: "    Hello World"
    assert clean_trailing_whitespace("    Hello World    ") == "    Hello World"

def test_preserve_inner_whitespace():
    # Input: "Hello    World" -> Expected: "Hello    World"
    assert clean_trailing_whitespace("Hello    World") == "Hello    World"

def test_trim_empty_text():
    # Input: "" -> Expected: ""
    assert clean_trailing_whitespace("") == ""

def test_preserve_unix_line_ending():
    # Input: "Line 1\nLine 2    \n" -> Expected: "Line 1\nLine 2\n"
    assert clean_trailing_whitespace("Line 1\nLine 2    \n") == "Line 1\nLine 2\n"

def test_preserve_windows_line_ending():
    # Input: "Line 1\r\nLine 2    \r\n" -> Expected: "Line 1\r\nLine 2\r\n"
    assert clean_trailing_whitespace("Line 1\r\nLine 2    \r\n") == "Line 1\r\nLine 2\r\n"

def test_mixed_line_endings():
    # Input: "Line 1\nLine 2\r\n" -> Expected: "Line 1\nLine 2\r\n"
    assert clean_trailing_whitespace("Line 1\nLine 2\r\n") == "Line 1\nLine 2\r\n"

def test_whitespace_line_keeps_line_ending():
    # Input: "    \n" -> Expected: "\n"
    assert clean_trailing_whitespace("    \n") == "\n"

def test_text_with_only_line_ending():
    # Input: "\n" -> Expected: "\n"
    assert clean_trailing_whitespace("\n") == "\n"

def test_text_with_only_windows_line_ending():
    # Input: "\r\n" -> Expected: "\r\n"
    assert clean_trailing_whitespace("\r\n") == "\r\n"

def test_lone_carriage_return_as_content():
    # Input: "Hello\rWorld" -> Expected: "Hello\rWorld"
    assert clean_trailing_whitespace("Hello\rWorld") == "Hello\rWorld"

def test_carriage_return_before_line_ending():
    # Input: "Hello\r\r\n" -> Expected: "Hello\r\r\n"
    assert clean_trailing_whitespace("Hello\r\r\n") == "Hello\r\r\n"

def test_carriage_return_with_trailing_whitespace():
    # Input: "Hello    \r    \n" -> Expected: "Hello    \r\n"
    assert clean_trailing_whitespace("Hello    \r    \n") == "Hello    \r\n"

def test_lone_carriage_return_at_end():
    # Input: "Hello\r" -> Expected: "Hello\r"
    assert clean_trailing_whitespace("Hello\r") == "Hello\r"

def test_non_final_line_with_trailing_spaces_and_final_line():
    # Input: "a \n\tb\t \r\nc  " -> Expected: "a\n\tb\r\nc"
    assert clean_trailing_whitespace("a \n\tb\t \r\nc  ") == "a\n\tb\r\nc"

def test_preserve_non_space_tab_whitespace_before_endings():
    # Input: "a\v\nb\f\r\n" -> Expected: "a\v\nb\f\r\n"
    assert clean_trailing_whitespace("a\v\nb\f\r\n") == "a\v\nb\f\r\n"

def test_preserve_internal_tabs():
    # Input: "a\tb" -> Expected: "a\tb"
    assert clean_trailing_whitespace("a\tb") == "a\tb"

def test_whitespace_only_windows_line():
    # Input: "\t \r\n" -> Expected: "\r\n"
    assert clean_trailing_whitespace("\t \r\n") == "\r\n"