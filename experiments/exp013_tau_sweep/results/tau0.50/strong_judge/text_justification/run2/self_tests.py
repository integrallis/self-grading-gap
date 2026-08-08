import pytest
from solution import justify_text

def test_single_word_fits_within_width():
    assert justify_text("Hello", 5) == ["Hello"]  # AC-1.1

def test_text_exactly_as_long_as_width():
    assert justify_text("Hello", 5) == ["Hello"]  # AC-1.2

def test_words_fitted_into_lines():
    assert justify_text("The quick brown fox", 16) == ["The  quick brown", "fox"]  # AC-1.3

def test_multiword_passage_fits_one_line():
    assert justify_text("a b", 5) == ["a b"]  # AC-1.1

def test_width_one_boundary():
    assert justify_text("a b c", 1) == ["a", "b", "c"]  # AC-1.3

def test_words_exactly_filling_later_line():
    assert justify_text("abc de fgh", 3) == ["abc", "de ", "fgh"]  # AC-1.3

def test_full_justification_with_multiple_words():
    assert justify_text("This is an example of text justification.", 16) == [
        "This    is    an",  # AC-2.6
        "example  of text",
        "justification."
    ]

def test_last_line_flush_left():
    assert justify_text("The quick brown fox", 10) == ["The  quick", "brown fox"]  # AC-2.4

def test_single_word_line_right_padded():
    assert justify_text("Hello world x", 6) == ["Hello ", "world ", "x"]  # AC-2.5

def test_large_word_on_own_line():
    assert justify_text("Supercalifragilisticexpialidocious", 10) == [
        "Supercalifragilisticexpialidocious"  # AC-3.1
    ]

def test_oversized_word_between_other_words():
    assert justify_text("Hello Supercalifragilisticexpialidocious World", 20) == [
        "Hello               ",  # AC-3.1
        "Supercalifragilisticexpialidocious",
        "World"
    ]

def test_tolerate_messy_source_spacing():
    assert justify_text("This    is  an   example.", 16) == ["This    is    an", "example."]  # AC-4.1

def test_tabs_and_newlines_as_word_separators():
    assert justify_text("This\tis\nan example.", 16) == ["This    is    an", "example."]  # AC-4.2

def test_empty_text_produces_no_lines():
    assert justify_text("", 10) == []  # AC-4.3

def test_whitespace_only_input():
    assert justify_text(" \t\n  ", 10) == []  # AC-4.3

def test_zero_width_refusal():
    with pytest.raises(Exception) as e:
        justify_text("Hello", 0)
    assert str(e.value) == "width must be a positive integer"  # AC-5.1

def test_negative_width_refusal():
    with pytest.raises(Exception) as e:
        justify_text("Hello", -1)
    assert str(e.value) == "width must be a positive integer"  # AC-5.1

def test_none_text_refusal():
    with pytest.raises(Exception) as e:
        justify_text(None, 10)
    assert str(e.value) == "text must not be None"  # AC-5.2