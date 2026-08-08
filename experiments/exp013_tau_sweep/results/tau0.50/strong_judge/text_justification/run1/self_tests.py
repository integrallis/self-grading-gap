import pytest
from solution import justify_text

def test_single_word_fits_within_width():
    # "Hi" fits within width 5
    assert justify_text("Hi", 5) == ["Hi"]

def test_single_word_exactly_as_long_as_width():
    # "Hello" fits exactly into width 5
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiple_words_fit_on_single_line():
    # "This is" fits within width 8
    assert justify_text("This is", 8) == ["This is"]

def test_multiple_words_with_padding():
    # "This is an" will be justified to width 12
    assert justify_text("This is an example", 12) == ["This  is  an", "example"]

def test_justification_with_padding():
    # "This is an" requires padding to width 12
    assert justify_text("This is an", 12) == ["This is an"]

def test_last_line_flush_left():
    # Canonical example
    assert justify_text("This is an example of text justification.", 16) == ["This    is    an", "example  of text", "justification."]

def test_single_long_word_on_its_own_line():
    # "Justification." is longer than width 10
    assert justify_text("Justification.", 10) == ["Justification."]

def test_tolerate_messy_source_spacing():
    # "This    is  an    example" treated as single spaces
    assert justify_text("This    is  an    example", 16) == ["This    is    an", "example"]

def test_empty_or_whitespace_text():
    # Empty string should produce no lines
    assert justify_text("", 10) == []
    assert justify_text("    ", 10) == []

def test_invalid_zero_width():
    # Invalid width of 0
    with pytest.raises(Exception, match=r"^width must be a positive integer$"):
        justify_text("Hello", 0)

def test_invalid_negative_width():
    # Invalid width of -1
    with pytest.raises(Exception, match=r"^width must be a positive integer$"):
        justify_text("Hello", -1)

def test_invalid_none_text():
    # Invalid None text
    with pytest.raises(Exception, match=r"^text must not be None$"):
        justify_text(None, 10)

def test_width_one_with_multiple_words():
    # Each word goes on its own line at width 1
    assert justify_text("This is an example", 1) == ["This", "is", "an", "example"]

def test_words_exactly_fill_a_later_line():
    # "aaaa bb ccc dd" with width 6 fills a later line exactly
    assert justify_text("aaaa bb ccc dd", 6) == ["aaaa  ", "bb ccc", "dd"]

def test_non_final_single_word_line_right_padded():
    # "Hi" should be right-padded at width 10
    assert justify_text("Hi", 10) == ["Hi        "]

def test_oversized_word_between_normal_words():
    # Oversized word "HelloWorld!" should be on its own line
    assert justify_text("Hi HelloWorld!", 10) == ["Hi", "HelloWorld!"]

def test_tabs_and_newlines_as_separators():
    # Tabs and newlines should be treated as spaces
    assert justify_text("This\tis\nan example", 16) == ["This    is    an", "example"]

def test_invalid_non_whole_width():
    # Invalid non-whole width of 2.5
    with pytest.raises(Exception, match=r"^width must be a positive integer$"):
        justify_text("Hello", 2.5)