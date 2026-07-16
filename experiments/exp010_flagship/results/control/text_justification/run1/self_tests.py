from solution import justify_text

def test_single_word_fits():
    # Input: "Hello", Width: 5
    # The word "Hello" fits exactly in the width of 5
    assert justify_text("Hello", 5) == ["Hello"]

def test_single_word_too_long():
    # Input: "HelloWorld", Width: 5
    # The word "HelloWorld" is too long, so it goes on its own line
    assert justify_text("HelloWorld", 5) == ["HelloWorld"]

def test_text_that_fits():
    # Input: "Hello World", Width: 11
    # The text "Hello World" fits exactly in the width of 11
    assert justify_text("Hello World", 11) == ["Hello World"]

def test_greedy_word_packing():
    # Input: "This is an example", Width: 16
    # "This is an" (11 chars) fits, next line "example" (7) fits with "of"
    assert justify_text("This is an example of text", 16) == ["This    is    an", "example  of text"]

def test_last_line_flush_left():
    # Input: "Justification", Width: 16
    # Last line should be flush left with no extra spaces
    assert justify_text("Justification", 16) == ["Justification"]

def test_single_word_with_padding():
    # Input: "Hello", Width: 10
    # "Hello" is a single word, should be right padded to width
    assert justify_text("Hello", 10) == ["Hello     "]

def test_tolerate_messy_spacing():
    # Input: "This   is\tan\nexample", Width: 16
    # All whitespace treated as a single space
    assert justify_text("This   is\tan\nexample", 16) == ["This    is    an", "example"]

def test_empty_or_whitespace_only_text():
    # Input: "", Width: 5
    # No lines should be produced for empty input
    assert justify_text("", 5) == []

def test_none_text():
    # Input: None, Width: 5
    # Should raise ValueError with message
    import pytest
    with pytest.raises(ValueError, match="text must not be None"):
        justify_text(None, 5)

def test_zero_width():
    # Input: "Hello", Width: 0
    # Should raise ValueError with message
    import pytest
    with pytest.raises(ValueError, match="width must be a positive integer"):
        justify_text("Hello", 0)

def test_negative_width():
    # Input: "Hello", Width: -5
    # Should raise ValueError with message
    import pytest
    with pytest.raises(ValueError, match="width must be a positive integer"):
        justify_text("Hello", -5)