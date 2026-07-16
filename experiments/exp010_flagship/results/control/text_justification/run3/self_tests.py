from solution import justify_text

def test_single_word_fits_within_width():
    # Text "Hello" fits within the width 10.
    assert justify_text("Hello", 10) == ["Hello"]

def test_single_word_exactly_as_long_as_width():
    # Text "Hello" is exactly 5 characters long, same as width 5.
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiple_words_filled_greedily():
    # "This is an example" at width 10 yields "This is", "an example".
    assert justify_text("This is an example", 10) == ["This is", "an example"]

def test_lines_with_exactly_filled_width():
    # "a b c d" at width 6 gives "a  b c", "d".
    assert justify_text("a b c d", 6) == ["a  b c", "d"]

def test_final_line_flush_left():
    # "This is an example of text justification." at width 16 yields:
    # "This    is    an", "example  of text", "justification."
    assert justify_text("This is an example of text justification.", 16) == ["This    is    an", "example  of text", "justification."]

def test_word_longer_than_width_on_own_line():
    # "HelloWorld" is longer than width 5 and goes alone.
    assert justify_text("HelloWorld", 5) == ["HelloWorld"]

def test_tolerate_messy_source_spacing():
    # "This   is  a test" with extra spaces should yield "This  is", "a test".
    assert justify_text("This   is  a test", 10) == ["This  is", "a test"]

def test_multiple_whitespace_as_single_separator():
    # "This   is  a     test" should yield "This  is", "a     test".
    assert justify_text("This   is  a     test", 10) == ["This  is", "a     test"]

def test_tabs_and_line_breaks_count_as_spaces():
    # "This\tis\na test" should yield "This is", "a test".
    assert justify_text("This\tis\na test", 10) == ["This is", "a test"]

def test_empty_or_whitespace_only_text_produces_no_lines():
    # Empty string should yield no lines.
    assert justify_text("", 10) == []
    # Whitespace only should yield no lines.
    assert justify_text("   \t\n", 10) == []

def test_zero_width_is_invalid():
    # Width 0 should raise an error.
    with pytest.raises(ValueError) as excinfo:
        justify_text("Hello", 0)
    assert str(excinfo.value) == "width must be a positive integer"

def test_negative_width_is_invalid():
    # Negative width should raise an error.
    with pytest.raises(ValueError) as excinfo:
        justify_text("Hello", -5)
    assert str(excinfo.value) == "width must be a positive integer"

def test_none_text_is_invalid():
    # None text should raise an error.
    with pytest.raises(ValueError) as excinfo:
        justify_text(None, 10)
    assert str(excinfo.value) == "text must not be None"