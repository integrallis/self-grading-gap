# test_fixed_width_text_justification.py

import pytest
from solution import justify_text

def test_single_line_fitting_text():
    # Input "Hello World" fits in width 11
    assert justify_text("Hello World", 11) == ["Hello World"]

def test_exact_width_text():
    # Input "HelloWorld" is exactly 10 characters, fitting in width 10
    assert justify_text("HelloWorld", 10) == ["HelloWorld"]

def test_greedy_word_packing():
    # Input "This is a test" at width 10 fits "This  is", "a test"
    assert justify_text("This is a test", 10) == ["This  is", "a test"]

def test_justification_with_padding():
    # Input "This is an example" at width 16 yields "This    is    an"
    # "example  of text" and "justification."
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_single_word_right_padding():
    # Input "Hello" at width 10 yields "Hello"
    assert justify_text("Hello", 10) == ["Hello"]

def test_final_line_flush_left():
    # Input "This is an example" at width 16 yields flush left final line
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_oversized_word_on_own_line():
    # Input "HelloWorld!" (11 chars) at width 10 pushes "HelloWorld!" alone
    assert justify_text("HelloWorld!", 10) == ["HelloWorld!"]

def test_tolerate_messy_spacing():
    # Input with extra spaces: "This    is  a   test" at width 10
    assert justify_text("This    is  a   test", 10) == ["This  is", "a test"]

def test_tabs_and_newlines_as_spaces():
    # Input with tabs and newlines: "This\tis\nan example" at width 16
    assert justify_text("This\tis\nan example", 16) == ["This    is    an", "example"]

def test_empty_text():
    # Empty input should yield no lines
    assert justify_text("", 10) == []

def test_whitespace_only_text():
    # Whitespace only input should yield no lines
    assert justify_text("  \t\n  ", 10) == []

def test_zero_width():
    # Zero width should raise an error
    with pytest.raises(Exception) as excinfo:
        justify_text("Hello World", 0)
    assert str(excinfo.value) == "width must be a positive integer"

def test_negative_width():
    # Negative width should raise an error
    with pytest.raises(Exception) as excinfo:
        justify_text("Hello World", -5)
    assert str(excinfo.value) == "width must be a positive integer"

def test_none_text():
    # None as text should raise an error
    with pytest.raises(Exception) as excinfo:
        justify_text(None, 10)
    assert str(excinfo.value) == "text must not be None"

def test_positive_non_whole_number_width():
    # Non-whole-number width should raise an error
    with pytest.raises(Exception):
        justify_text("Hello World", 10.5)

def test_width_one():
    # Input "a bb c" at width 1 yields each word on its own line
    assert justify_text("a bb c", 1) == ["a", "bb", "c"]

def test_later_line_exactly_fills_width():
    # Input "a b cc dd ee" at width 5 yields "a   b", "cc dd", "ee"
    assert justify_text("a b cc dd ee", 5) == ["a   b", "cc dd", "ee"]

def test_non_final_one_word_line_padding():
    # Input "a longword" at width 5 yields "a    ", "longword"
    assert justify_text("a longword", 5) == ["a    ", "longword"]

def test_oversize_word_in_context():
    # Input "a enormous b" at width 5 yields "a    ", "enormous", "b"
    assert justify_text("a enormous b", 5) == ["a    ", "enormous", "b"]