import pytest
from solution import justify_text

def test_flow_words_onto_lines():
    # AC-1.1: Text that fits within the width comes back as a single line, unchanged
    assert justify_text("hi there", 10) == ["hi there"]  # strictly shorter than width
    assert justify_text("Hello", 5) == ["Hello"]  # fits within width 5
    # AC-1.2: Text exactly as long as the width fits on one line
    assert justify_text("Hello", 5) == ["Hello"]  # exactly 5 characters
    # AC-1.3: Words are packed greedily
    assert justify_text("This is an example", 14) == ["This   is   an", "example"]  # fits 14 chars
    assert justify_text("This is an example of text", 16) == ["This    is    an", "example of text"]  # canonical example
    assert justify_text("Hello world", 11) == ["Hello world"]  # fits exactly
    assert justify_text("a b c", 1) == ["a", "b", "c"]  # width 1, each word on its own line
    assert justify_text("long aa bb", 5) == ["long ", "aa bb"]  # later line exactly fills width
    assert justify_text("Hello a World", 5) == ["Hello", "a    ", "World"]  # correct padding for a single word line

def test_justify_to_both_margins():
    # AC-2.1: Every line except the last is padded to exactly the column width
    assert justify_text("This is an example", 14) == ["This   is   an", "example"]  # padding not needed for last
    # AC-2.2: Padding spaces are distributed across the gaps
    assert justify_text("a b c d", 6) == ["a  b c", "d"]  # padding spaces distributed
    # AC-2.3: Leftover spaces go to the leftmost gaps
    assert justify_text("a b c d", 7) == ["a b c d"]  # all words fit exactly
    # AC-2.4: The final line sits flush-left
    assert justify_text("This is an example", 14) == ["This   is   an", "example"]  # last line flush-left
    # AC-2.5: A line before the last that carries a single word is right-padded
    assert justify_text("Hello a", 6) == ["Hello ", "a"]  # non-final single-word line

    # AC-2.6: Canonical worked example
    assert justify_text("This is an example of text justification.", 16) == ["This    is    an", "example  of text", "justification."]

def test_keep_oversize_words_whole():
    # AC-3.1: A word longer than the width is placed alone on its own line
    assert justify_text("HelloWorld", 5) == ["HelloWorld"]  # alone on its own line
    assert justify_text("aa HelloWorld bb", 5) == ["aa   ", "HelloWorld", "bb"]  # oversize word surrounded by other words

def test_tolerate_messy_source_spacing():
    # AC-4.1: Consecutive blanks in the source count as a single separator
    assert justify_text("Hello    world", 11) == ["Hello world"]  # consecutive spaces
    # AC-4.2: Tabs and line breaks separate words exactly like spaces
    assert justify_text("Hello\tworld", 11) == ["Hello world"]  # tab as separator
    assert justify_text("Hello\nworld", 11) == ["Hello world"]  # newline as separator
    # AC-4.3: Empty or whitespace-only text produces no lines at all
    assert justify_text("", 10) == []  # empty text
    assert justify_text("   ", 10) == []  # whitespace-only text

def test_refuse_invalid_requests():
    # AC-5.1: The column width must be a positive whole number
    with pytest.raises(Exception, match="^width must be a positive integer$"):
        justify_text("Hello", 0)  # zero width
    with pytest.raises(Exception, match="^width must be a positive integer$"):
        justify_text("Hello", -5)  # negative width
    with pytest.raises(Exception, match="^width must be a positive integer$"):
        justify_text("Hello", 1.5)  # non-whole width

    # AC-5.2: A missing text is refused
    with pytest.raises(Exception, match="^text must not be None$"):
        justify_text(None, 10)  # None text