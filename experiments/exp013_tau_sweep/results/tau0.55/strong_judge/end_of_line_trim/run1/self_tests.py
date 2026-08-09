def test_remove_trailing_space():
    # Input: "This is a line with trailing space    \n"
    # Expected output: "This is a line with trailing space\n"
    assert trailing_whitespace_cleaner("This is a line with trailing space    \n") == "This is a line with trailing space\n"

def test_remove_trailing_tab():
    # Input: "This is a line with trailing tab\t\n"
    # Expected output: "This is a line with trailing tab\n"
    assert trailing_whitespace_cleaner("This is a line with trailing tab\t\n") == "This is a line with trailing tab\n"

def test_remove_mixed_trailing_whitespace():
    # Input: "This line has mixed whitespace   \t\n"
    # Expected output: "This line has mixed whitespace\n"
    assert trailing_whitespace_cleaner("This line has mixed whitespace   \t\n") == "This line has mixed whitespace\n"

def test_trim_final_line_with_no_ending():
    # Input: "Final line with trailing space    "
    # Expected output: "Final line with trailing space"
    assert trailing_whitespace_cleaner("Final line with trailing space    ") == "Final line with trailing space"

def test_only_spaces_and_tabs_removed():
    # Input: "Content with a special character *\n"
    # Expected output: "Content with a special character *\n"
    assert trailing_whitespace_cleaner("Content with a special character *\n") == "Content with a special character *\n"

def test_no_trailing_whitespace_returned_unchanged():
    # Input: "No trailing whitespace here.\n"
    # Expected output: "No trailing whitespace here.\n"
    assert trailing_whitespace_cleaner("No trailing whitespace here.\n") == "No trailing whitespace here.\n"

def test_preserve_leading_whitespace():
    # Input: "   Leading whitespace preserved\n"
    # Expected output: "   Leading whitespace preserved\n"
    assert trailing_whitespace_cleaner("   Leading whitespace preserved\n") == "   Leading whitespace preserved\n"

def test_preserve_leading_tabs():
    # Input: "\tfirst\n  \tsecond\n"
    # Expected output: "\tfirst\n  \tsecond\n"
    assert trailing_whitespace_cleaner("\tfirst\n  \tsecond\n") == "\tfirst\n  \tsecond\n"

def test_preserve_inner_whitespace():
    # Input: "Inner whitespace    between words\n"
    # Expected output: "Inner whitespace    between words\n"
    assert trailing_whitespace_cleaner("Inner whitespace    between words\n") == "Inner whitespace    between words\n"

def test_empty_text_trims_to_empty_text():
    # Input: ""
    # Expected output: ""
    assert trailing_whitespace_cleaner("") == ""

def test_keep_unix_line_ending():
    # Input: "Line with Unix ending\n"
    # Expected output: "Line with Unix ending\n"
    assert trailing_whitespace_cleaner("Line with Unix ending\n") == "Line with Unix ending\n"

def test_keep_windows_line_ending():
    # Input: "Line with Windows ending\r\n"
    # Expected output: "Line with Windows ending\r\n"
    assert trailing_whitespace_cleaner("Line with Windows ending\r\n") == "Line with Windows ending\r\n"

def test_preserve_mixed_line_endings():
    # Input: "First line\nSecond line\r\nThird line\n"
    # Expected output: "First line\nSecond line\r\nThird line\n"
    assert trailing_whitespace_cleaner("First line\nSecond line\r\nThird line\n") == "First line\nSecond line\r\nThird line\n"

def test_whitespace_line_keeps_line_ending():
    # Input: "   \n"
    # Expected output: "\n"
    assert trailing_whitespace_cleaner("   \n") == "\n"

def test_text_with_only_line_ending_kept_unchanged():
    # Input: "\r\n"
    # Expected output: "\r\n"
    assert trailing_whitespace_cleaner("\r\n") == "\r\n"

def test_carriage_return_as_content():
    # Input: "Text with carriage return here\rText with content\n"
    # Expected output: "Text with carriage return here\rText with content\n"
    assert trailing_whitespace_cleaner("Text with carriage return here\rText with content\n") == "Text with carriage return here\rText with content\n"

def test_preserve_whitespace_before_lone_carriage_return():
    # Input: "Text with space before carriage return \r\n"
    # Expected output: "Text with space before carriage return\r\n"
    assert trailing_whitespace_cleaner("Text with space before carriage return \r\n") == "Text with space before carriage return\r\n"

def test_whitespace_after_lone_carriage_return_removed():
    # Input: "Content before\r   \n"
    # Expected output: "Content before\r\n"
    assert trailing_whitespace_cleaner("Content before\r   \n") == "Content before\r\n"

def test_terminal_lone_carriage_return_preserved():
    # Input: "data\r"
    # Expected output: "data\r"
    assert trailing_whitespace_cleaner("data\r") == "data\r"

def test_lone_carriage_return_kept_as_content():
    # Input: "a \r\t\n"
    # Expected output: "a \r\n"
    assert trailing_whitespace_cleaner("a \r\t\n") == "a \r\n"

def test_content_carriage_return_before_windows_line_ending():
    # Input: "a\r\r\n"
    # Expected output: "a\r\r\n"
    assert trailing_whitespace_cleaner("a\r\r\n") == "a\r\r\n"

def test_whitespace_only_crlf_line_keeps_line_ending():
    # Input: "\t  \r\n"
    # Expected output: "\r\n"
    assert trailing_whitespace_cleaner("\t  \r\n") == "\r\n"

def test_multi_line_trimming():
    # Input: "first  \n\tsecond\t\r\nfinal \t"
    # Expected output: "first\n\tsecond\r\nfinal"
    assert trailing_whitespace_cleaner("first  \n\tsecond\t\r\nfinal \t") == "first\n\tsecond\r\nfinal"