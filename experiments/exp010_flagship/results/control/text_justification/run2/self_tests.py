import pytest
from solution import justify_text

def test_single_word_fits_within_width():
    # "Hello" is 5 characters, width is 10
    assert justify_text("Hello", 10) == ["Hello"]

def test_text_fits_exactly_one_line():
    # "Hello World" is 11 characters, width is 11
    assert justify_text("Hello World", 11) == ["Hello World"]

def test_words_packed_greedily():
    # "This is an example" fits into width 16 as "This    is    an" and "example"
    assert justify_text("This is an example", 16) == ["This    is    an", "example"]

def test_last_line_flush_left():
    # "This is an example of text justification." at width 16 gives
    # "This    is    an", "example  of text", "justification."
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_single_word_on_its_own_line():
    # "extraordinarily" is longer than width 10
    assert justify_text("extraordinarily", 10) == ["extraordinarily"]

def test_consecutive_spaces_treated_as_one():
    # "This   is    an example" becomes "This    is    an"
    assert justify_text("This   is    an example", 16) == ["This    is    an", "example"]

def test_tabs_and_newlines_as_separators():
    # "This\tis\nan example" treated like spaces
    assert justify_text("This\tis\nan example", 16) == ["This    is    an", "example"]

def test_empty_input_produces_no_lines():
    # Empty string produces no lines
    assert justify_text("", 10) == []

def test_whitespace_only_input_produces_no_lines():
    # Whitespace only produces no lines
    assert justify_text("    \t  \n  ", 10) == []

def test_invalid_width_zero():
    # Invalid width of 0
    with pytest.raises(ValueError) as excinfo:
        justify_text("Any text", 0)
    assert str(excinfo.value) == "width must be a positive integer"

def test_invalid_width_negative():
    # Invalid width of -5
    with pytest.raises(ValueError) as excinfo:
        justify_text("Any text", -5)
    assert str(excinfo.value) == "width must be a positive integer"

def test_invalid_width_non_integer():
    # Invalid width of "ten"
    with pytest.raises(ValueError) as excinfo:
        justify_text("Any text", "ten")
    assert str(excinfo.value) == "width must be a positive integer"

def test_missing_text():
    # Missing text is None
    with pytest.raises(ValueError) as excinfo:
        justify_text(None, 10)
    assert str(excinfo.value) == "text must not be None"