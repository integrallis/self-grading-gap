from solution import clean_trailing_whitespace

def test_remove_trailing_whitespace_from_every_line():
    # AC-1.1: A trailing space at the end of a line is removed.
    assert clean_trailing_whitespace("Hello World!    \n") == "Hello World!\n"  # "    " removed
    # AC-1.2: A trailing tab at the end of a line is removed.
    assert clean_trailing_whitespace("Hello World!\t\n") == "Hello World!\n"  # "\t" removed
    # AC-1.3: A mixed run of trailing spaces and tabs is removed entirely.
    assert clean_trailing_whitespace("Hello World!    \t\n") == "Hello World!\n"  # "    \t" removed
    # AC-1.4: Every line of a multi-line text is trimmed — including the final line when it has no line ending.
    assert clean_trailing_whitespace("Line 1    \nLine 2    \nLine 3\n") == "Line 1\nLine 2\nLine 3\n"  # "    " removed from each line
    # AC-1.5: Only spaces and tabs are ever removed; any other character at the end of a line stays, on every line-ending style.
    assert clean_trailing_whitespace("Line 1 !\nLine 2 #\n") == "Line 1 !\nLine 2 #\n"  # no trailing whitespace

def test_preserve_all_other_whitespace_and_content():
    # AC-2.1: Text containing no trailing whitespace is returned unchanged.
    assert clean_trailing_whitespace("Hello World!\n") == "Hello World!\n"  # unchanged
    # AC-2.2: Leading spaces and tabs at the start of a line are preserved, on every line.
    assert clean_trailing_whitespace("    Hello\n\tWorld\n") == "    Hello\n\tWorld\n"  # unchanged
    # AC-2.3: Whitespace between words inside a line is untouched.
    assert clean_trailing_whitespace("Hello   World\n") == "Hello   World\n"  # no change to internal whitespace
    # AC-2.4: The empty text trims to the empty text.
    assert clean_trailing_whitespace("") == ""  # unchanged

def test_keep_each_lines_original_ending():
    # AC-3.1: A Unix line ending (`\n`) is kept as-is.
    assert clean_trailing_whitespace("Line 1\nLine 2\n") == "Line 1\nLine 2\n"  # unchanged
    # AC-3.2: A Windows line ending (`\r\n`) is kept as-is; trailing whitespace just before it is removed.
    assert clean_trailing_whitespace("Line 1    \r\nLine 2    \r\n") == "Line 1\r\nLine 2\r\n"  # trailing "    " removed
    # AC-3.3: Unix and Windows endings mixed within a single text are each preserved where they occur.
    assert clean_trailing_whitespace("Line 1    \r\nLine 2\n") == "Line 1\r\nLine 2\n"  # trailing "    " removed
    # AC-3.4: A line consisting only of whitespace keeps just its line ending.
    assert clean_trailing_whitespace("    \n\r\n") == "\n\r\n"  # spaces are removed, keeping line endings
    # AC-3.5: A text consisting solely of a line ending (`\n` alone, or `\r\n` alone) is returned unchanged.
    assert clean_trailing_whitespace("\n") == "\n"  # unchanged
    assert clean_trailing_whitespace("\r\n") == "\r\n"  # unchanged

def test_treat_lone_carriage_returns_as_content():
    # AC-4.1: A carriage return not followed by a line feed does not end a line; it stays in place as content.
    assert clean_trailing_whitespace("Hello\r") == "Hello\r"  # unchanged
    # AC-4.2: Whitespace before such a carriage return is interior, not trailing, and is preserved.
    assert clean_trailing_whitespace("Hello   \r  \n") == "Hello   \r\n"  # trailing spaces before \n removed, \r kept
    # AC-4.3: A content carriage return sitting immediately before a Windows line ending survives.
    assert clean_trailing_whitespace("a\r\r\n") == "a\r\r\n"  # first \r is content, second is part of \r\n