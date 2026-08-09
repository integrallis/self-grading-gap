import pytest

def test_single_word_fits_within_width():
    # "Hello" fits within width 5
    assert justify_text("Hello", 5) == ["Hello"]

def test_single_word_exactly_as_long_as_width():
    # "Hello" is exactly 5 characters long, fits in width 5
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiple_words_fit_within_width():
    # "This is" fits within width 8
    assert justify_text("This is", 8) == ["This is"]

def test_flow_words_greedily():
    # "This is an example" with width 10 fits as "This is an", "example"
    assert justify_text("This is an example", 10) == ["This is an", "example"]

def test_full_justification():
    # "This is an example" at width 16
    # "This    is    an" has spaces distributed to fill width 16
    # "example  of text" similarly fills width 16
    # "justification." is the last line, flush-left
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",
        "example  of text",
        "justification."
    ]

def test_keep_oversize_words():
    # "supercalifragilisticexpialidocious" is longer than width 10
    # It stays alone on its line
    assert justify_text("supercalifragilisticexpialidocious", 10) == [
        "supercalifragilisticexpialidocious"
    ]

def test_oversize_word_within_normal_flow():
    # "This is a supercalifragilisticexpialidocious test" 
    # should fit "This  is a", "supercalifragilisticexpialidocious", "test"
    assert justify_text("This is a supercalifragilisticexpialidocious test", 10) == [
        "This  is a",
        "supercalifragilisticexpialidocious",
        "test"
    ]

def test_tolerate_messy_source_spacing():
    # "This   is a   test" with messy spacing treated as "This is a test"
    assert justify_text("This   is a   test", 10) == ["This  is a", "test"]

def test_tolerate_tabs_and_newlines():
    # "This\tis\na test" should be treated as "This is a test"
    assert justify_text("This\tis\na test", 10) == ["This  is a", "test"]

def test_empty_or_whitespace_only_text():
    # Empty text should produce no lines
    assert justify_text("", 5) == []
    # Whitespace only should also produce no lines
    assert justify_text("    \t\n", 5) == []

def test_refuse_invalid_requests_negative_width():
    # Negative width is invalid
    with pytest.raises(Exception) as exc_info:
        justify_text("Hello", -1)
    assert str(exc_info.value) == "width must be a positive integer"

def test_refuse_invalid_requests_zero_width():
    # Zero width is invalid
    with pytest.raises(Exception) as exc_info:
        justify_text("Hello", 0)
    assert str(exc_info.value) == "width must be a positive integer"

def test_refuse_invalid_requests_none_width():
    # None width is invalid
    with pytest.raises(Exception) as exc_info:
        justify_text("Hello", None)
    assert str(exc_info.value) == "width must be a positive integer"

def test_refuse_invalid_requests_missing_text():
    # None text is invalid
    with pytest.raises(Exception) as exc_info:
        justify_text(None, 5)
    assert str(exc_info.value) == "text must not be None"

def test_non_final_single_word_right_padding():
    # "a bbbb" at width 4 must have "a   " and "bbbb"
    assert justify_text("a bbbb", 4) == ["a   ", "bbbb"]

def test_positive_non_whole_numeric_width():
    # Non-whole numeric width is invalid (e.g., float)
    with pytest.raises(Exception) as exc_info:
        justify_text("Hello", 2.5)
    assert str(exc_info.value) == "width must be a positive integer"

def test_width_one_behavior():
    # "a b c" at width 1 should result in each word on a new line
    assert justify_text("a b c", 1) == ["a", "b", "c"]

def test_words_filling_later_line():
    # "a bb ccc dd" at width 6 should yield "a    bb", "ccc dd"
    assert justify_text("a bb ccc dd", 6) == ["a    bb", "ccc dd"]