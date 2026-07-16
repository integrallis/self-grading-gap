# your complete test file
from solution import wrap_text

def test_wrap_text_unmodified_within_width():
    assert wrap_text("ab cd", 5) == "ab cd"  # fits exactly at width 5
    assert wrap_text("Hello", 5) == "Hello"  # fits within width 5
    assert wrap_text("hi", 5) == "hi"  # fits within width 5

def test_wrap_text_breaks_at_last_space():
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # breaks at last space
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # breaks at last space

def test_wrap_text_hard_split_long_word():
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # hard-splits long word

def test_wrap_text_single_character_first_word():
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # breaks at space after single character

def test_wrap_text_column_count_restarts_after_break():
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # column counting restarts after break

def test_wrap_text_empty_input():
    assert wrap_text("", 5) == ""  # no text provided
    assert wrap_text(" ", 5) == ""  # whitespace-only
    assert wrap_text("\t", 5) == ""  # single tab input

def test_wrap_text_trailing_spaces_dropped():
    assert wrap_text("hi  ", 2) == "hi"  # trailing spaces dropped

def test_wrap_text_line_breaks_preserved():
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # breaks around existing line breaks
    assert wrap_text("\n\nLet's Go\noutside.", 5) == "\n\nLet's\nGo\noutsi\nde."  # consecutive line breaks preserved

def test_wrap_text_column_count_restarts_after_existing_break():
    assert wrap_text("abc\ndefghi", 4) == "abc\ndefg\nhi"  # column counting restarts after line break

def test_wrap_text_segments_fit_within_width():
    assert wrap_text("abc\ndef", 4) == "abc\ndef"  # segments fit within width

def test_wrap_text_only_spaces_consumed_at_break():
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # tab survives after break
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # 'X' survives after break

def test_wrap_text_tab_indent_preserved_after_break():
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # tab indentation preserved

def test_wrap_text_space_at_start_does_not_break():
    assert wrap_text(" hello", 3) == " he\nllo"  # hard-break at width instead of space