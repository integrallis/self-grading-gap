# your complete test file
from solution import wrap_text

def test_wrap_text_fits_within_width():
    assert wrap_text("ab cd", 5) == "ab cd"  # AC-1.1
    assert wrap_text("hello", 5) == "hello"  # AC-1.1

def test_wrap_text_breaks_at_last_space():
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # AC-1.2
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # AC-1.2

def test_wrap_text_hard_split_long_words():
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # AC-1.3

def test_wrap_text_breaks_single_letter_first_word():
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # AC-1.4

def test_wrap_text_column_count_resets_after_break():
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # AC-1.5

def test_wrap_text_empty_input():
    assert wrap_text("", 5) == ""  # AC-2.1
    # The specification does not define None as an input, so we do not test it.

def test_wrap_text_whitespace_only_input():
    assert wrap_text(" ", 5) == ""  # AC-2.2
    assert wrap_text("\t", 5) == ""  # AC-2.2

def test_wrap_text_trailing_spaces_dropped():
    assert wrap_text("hi  ", 2) == "hi"  # AC-2.3

def test_wrap_text_preserves_line_breaks():
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # AC-3.1
    assert wrap_text("\n\nLet's Go\noutside.", 5) == "\n\nLet's\nGo\noutsi\nde."  # AC-3.2
    assert wrap_text("abc\nxyz", 4) == "abc\nxyz"  # AC-3.3
    assert wrap_text("abc\nxy", 4) == "abc\nxy"  # AC-3.4

def test_wrap_text_consume_only_spaces():
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # AC-4.1
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # AC-4.2
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # AC-4.3
    assert wrap_text(" hello", 3) == " he\nllo"  # AC-4.4