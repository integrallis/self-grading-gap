import pytest
from solution import justify_text

def test_single_word_within_width():
    # "Hello" fits within width 5 as a single line.
    assert justify_text("Hello", 5) == ["Hello"]

def test_single_word_exact_width():
    # "Hello" is exactly length 5, it fills the width.
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiple_words_fit_on_one_line():
    # "Hello World" fits within width 11 as a single line.
    assert justify_text("Hello World", 11) == ["Hello World"]

def test_greedy_word_packing():
    # "This is an example" with width 16 should yield ["This    is    an", "example"].
    assert justify_text("This is an example", 16) == ["This    is    an", "example"]

def test_padding_spaces_distribution():
    # "a b c d" at width 6 gives "a  b c" then "d".
    assert justify_text("a b c d", 6) == ["a  b c", "d"]

def test_final_line_flush_left():
    # The final line should sit flush-left: "example of text".
    assert justify_text("example of text", 16) == ["example of text"]

def test_single_word_on_own_line():
    # A long word "supercalifragilisticexpialidocious" should overflow.
    assert justify_text("supercalifragilisticexpialidocious", 10) == ["supercalifragilisticexpialidocious"]

def test_tolerate_messy_spacing():
    # Multiple spaces and a tab should be treated as single separators.
    assert justify_text("This  is\ta test", 10) == ["This  is a", "test"]

def test_empty_text():
    # Empty text should produce no lines.
    assert justify_text("", 10) == []

def test_whitespace_only_text():
    # Whitespace-only text should produce no lines.
    assert justify_text("   \t\n", 10) == []

def test_zero_width():
    # A zero width should raise an error.
    with pytest.raises(Exception) as excinfo:
        justify_text("text", 0)
    assert str(excinfo.value) == "width must be a positive integer"

def test_negative_width():
    # A negative width should raise an error.
    with pytest.raises(Exception) as excinfo:
        justify_text("text", -5)
    assert str(excinfo.value) == "width must be a positive integer"

def test_non_whole_width():
    # A non-whole width should raise an error.
    with pytest.raises(Exception) as excinfo:
        justify_text("text", 2.5)
    assert str(excinfo.value) == "width must be a positive integer"

def test_none_text():
    # None text should raise an error.
    with pytest.raises(Exception) as excinfo:
        justify_text(None, 5)
    assert str(excinfo.value) == "text must not be None"

def test_single_word_overflow():
    # A single word longer than the width should overflow.
    assert justify_text("HelloWorld", 5) == ["HelloWorld"]

def test_single_word_right_padding():
    # A single word should be right-padded when it is the only word on the line.
    assert justify_text("Hello", 10) == ["Hello"]

def test_canonical_example():
    # Testing the canonical example given in the specification.
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_short_single_final_word():
    # A single short word fits within the width as the final line.
    assert justify_text("Hello", 10) == ["Hello"]

def test_width_one_flow():
    # At width 1, each word gets its own line.
    assert justify_text("a b c", 1) == ["a", "b", "c"]

def test_later_words_fill_line():
    # Words exactly filling a later line.
    assert justify_text("aa b cc dd e", 5) == ["aa  b", "cc dd", "e"]

def test_single_word_non_final_line():
    # A single word non-final line should be padded.
    assert justify_text("hi there x", 5) == ["hi   ", "there", "x"]

def test_oversize_word_amid_other_words():
    # An oversize word placed amid other words.
    assert justify_text("a toolong b", 3) == ["a  ", "toolong", "b"]

def test_line_break_normalization():
    # Line breaks should be treated as spaces.
    assert justify_text("a\nb", 10) == ["a b"]