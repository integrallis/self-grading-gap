import pytest
from solution import justify_text

def test_single_line_fit():
    # "Hello" fits within width 5
    assert justify_text("Hello", 5) == ["Hello"]

def test_exact_width_fit():
    # "Hello" is exactly 5 characters long, fits in one line
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiword_input_fitting_width():
    # "a b" fits within width 3
    assert justify_text("a b", 3) == ["a b"]

def test_greedy_word_packing():
    # "This is" fits in width 8: "This  is"
    # "an" is a single-word non-final line: "an      "
    # "example" is a single-word non-final line: "example "
    # "of text" fits in width 8: "of  text"
    # "justification." is the last line and remains unpadded.
    assert justify_text("This is an example of text justification.", 8) == ["This  is", "an      ", "example ", "of  text", "justification."]

def test_full_justification():
    # "This is an" has 8 word characters, so its two gaps receive 2 spaces: "This  is  an"
    # "example of" has 9 word characters and one gap, which receives 3 spaces: "example   of"
    # "text" is the final line.
    assert justify_text("This is an example of text", 12) == ["This  is  an", "example   of", "text"]

def test_final_line_flush_left():
    # Last line "justification." should be flush-left
    assert justify_text("This is an example of text justification.", 16) == ["This    is    an", "example  of text", "justification."]

def test_keep_oversize_words():
    # "hello" is 5, "world" is 5, "oversizedword" is 15 which exceeds width 10
    assert justify_text("hello world oversizedword", 10) == ["hello     ", "world     ", "oversizedword"]

def test_keep_oversize_word_alone():
    # "oversizedword" is 15 which exceeds width 10 and is the only word
    assert justify_text("oversizedword", 10) == ["oversizedword"]

def test_tolerate_messy_spacing():
    # After whitespace normalization, the words are:
    # "This is a test. New line and more spacing."
    assert justify_text("This   is    a test.\n\nNew line\tand more spacing.", 16) == ["This  is a test.", "New   line   and", "more spacing."]

def test_empty_or_whitespace_text():
    # Empty string should produce no lines
    assert justify_text("", 5) == []
    # Whitespace-only text should also produce no lines
    assert justify_text("     \n\t", 5) == []

def test_invalid_width_zero():
    # Invalid width should be refused with a message
    with pytest.raises(ValueError, match="width must be a positive integer"):
        justify_text("Hello", 0)

def test_invalid_width_negative():
    # Invalid width should be refused with a message
    with pytest.raises(ValueError, match="width must be a positive integer"):
        justify_text("Hello", -5)

def test_invalid_width_non_whole():
    # Invalid width (non-whole number) should be refused with a message
    with pytest.raises(ValueError, match="width must be a positive integer"):
        justify_text("Hello", 1.5)

def test_missing_text():
    # Missing text should be refused with a message
    with pytest.raises(ValueError, match="text must not be None"):
        justify_text(None, 5)

def test_width_one():
    # At width one, every word gets its own line
    assert justify_text("a b c", 1) == ["a", "b", "c"]

def test_exactly_filled_later_line():
    # "aaaa" fills width 5, followed by "b ccc" fills width 5 as well
    assert justify_text("aaaa b ccc dd", 5) == ["aaaa ", "b ccc", "dd"]

def test_non_final_single_word_padding():
    # "hello" fits in width 6, "x" is a non-final single-word line: "x"
    assert justify_text("hello x", 6) == ["hello ", "x"]