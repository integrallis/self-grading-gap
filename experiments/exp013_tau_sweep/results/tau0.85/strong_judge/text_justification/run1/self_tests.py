import pytest
from solution import justify_text

def test_single_short_word():
    # Input: "Hello", width: 5
    # The text fits within the width, unchanged.
    assert justify_text("Hello", 5) == ["Hello"]

def test_text_fits_exactly():
    # Input: "Hello", width: 5
    # The text fits exactly as long as the width.
    assert justify_text("Hello", 5) == ["Hello"]

def test_words_packed_greedily():
    # Input: "This is an example", width: 14
    # Should be packed as: "This   is   an", "example"
    assert justify_text("This is an example", 14) == ["This   is   an", "example"]

def test_single_word_each_line_at_width_one():
    # Input: "a b c", width: 1
    # Every word gets its own line.
    assert justify_text("a b c", 1) == ["a", "b", "c"]

def test_full_justification():
    # Input: "This is an example", width: 16
    # Should justify to: "This    is    an", "example  of text", "justification."
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_last_line_flush_left():
    # Input: "This is an example", width: 14
    # The last line is flush-left: "example"
    assert justify_text("This is an example", 14) == ["This   is   an", "example"]

def test_pad_single_word_line():
    # Input: "Hello", width: 10
    # Should be flush-left: "Hello"
    assert justify_text("Hello", 10) == ["Hello"]

def test_single_long_word_on_own_line():
    # Input: "Supercalifragilisticexpialidocious", width: 10
    # The long word goes on its own line, overflowing.
    assert justify_text("Supercalifragilisticexpialidocious", 10) == [
        "Supercalifragilisticexpialidocious"
    ]

def test_tolerate_messy_whitespace():
    # Input: "This   is   an example", width: 14
    # Should be treated as: "This   is   an", "example"
    assert justify_text("This   is   an example", 14) == ["This   is   an", "example"]

def test_consecutive_blanks_count_as_one_separator():
    # Input: "This    is", width: 10
    # Should be treated as: "This is"
    assert justify_text("This    is", 10) == ["This is"]

def test_empty_string():
    # Input: "", width: 5
    # Should produce no lines at all.
    assert justify_text("", 5) == []

def test_whitespace_only():
    # Input: "   ", width: 5
    # Should produce no lines at all.
    assert justify_text("   ", 5) == []

def test_zero_width():
    # Input: "Hello", width: 0
    # Should refuse with specific message.
    assert justify_text("Hello", 0) == "width must be a positive integer"

def test_negative_width():
    # Input: "Hello", width: -5
    # Should refuse with specific message.
    assert justify_text("Hello", -5) == "width must be a positive integer"

def test_non_whole_number_width():
    # Input: "Hello", width: 1.5
    # Should refuse with specific message.
    assert justify_text("Hello", 1.5) == "width must be a positive integer"

def test_none_text():
    # Input: None, width: 5
    # Should refuse with specific message.
    assert justify_text(None, 5) == "text must not be None"

def test_oversize_word_among_other_words():
    # Input: "hi enormously ok", width: 5
    # The oversize word goes on its own line, overflowing.
    assert justify_text("hi enormously ok", 5) == ["hi   ", "enormously", "ok"]

def test_tabs_and_newlines_normalization():
    # Input: "a\tb\nc", width: 3
    # Should treat tabs and newlines as spaces: "a b", "c"
    assert justify_text("a\tb\nc", 3) == ["a b", "c"]

def test_greedy_flow_with_exactly_filled_later_line():
    # Input: "aa bb ccc dd e", width: 6
    # Should be packed as: "aa  bb", "ccc dd", "e"
    assert justify_text("aa bb ccc dd e", 6) == ["aa  bb", "ccc dd", "e"]