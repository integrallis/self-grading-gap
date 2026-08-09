from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: Text that already fits within the width is returned unchanged
    assert wrap_text("ab cd", 5) == "ab cd"  # fits exactly
    assert wrap_text("abc", 5) == "abc"      # fits within the width
    assert wrap_text("abcde", 5) == "abcde"  # exactly-width line without space

def test_wrap_text_exceeds_width():
    # AC-1.2: Break at the last space
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # breaks at last space
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # multiple breaks

def test_wrap_text_hard_split():
    # AC-1.3: Hard-split a single long word
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # hard-split at width

def test_wrap_text_single_word_and_space():
    # AC-1.4: Breaks at the space for a one-letter first word
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # breaks at space

def test_wrap_text_restart_counting_after_break():
    # AC-1.5: Column counting restarts after an inserted break
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # no further break

def test_wrap_text_empty_and_whitespace_input():
    # AC-2.1: No text results in empty string
    assert wrap_text("", 5) == ""  # empty input
    # AC-2.2: Whitespace-only text produces empty string
    assert wrap_text(" ", 5) == ""  # single space
    assert wrap_text("\t", 5) == ""  # single tab

def test_wrap_text_trailing_spaces():
    # AC-2.3: Trailing spaces are dropped
    assert wrap_text("hi  ", 2) == "hi"  # trailing spaces dropped

def test_wrap_text_respects_line_breaks():
    # AC-3.1: Existing line breaks are kept, text wraps independently
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # breaks independently
    # AC-3.2: Consecutive line breaks are preserved
    assert wrap_text("\n\nLet's Go\noutside.", 5) == "\n\nLet's\nGo\noutsi\nde."  # multiple breaks

def test_wrap_text_column_counting_restarts():
    # AC-3.3: Column counting restarts after a line break
    assert wrap_text("abc\nabc", 4) == "abc\nabc"  # fits on either side of break

def test_wrap_text_segments_fit_within_width():
    # AC-3.4: Segments around an existing break that fit within the width stay exactly as they are
    assert wrap_text("abc\ndef", 4) == "abc\ndef"  # both fit

def test_wrap_text_consume_spaces_only():
    # AC-4.1: Only spaces are consumed at a break
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # tab survives

def test_wrap_text_characters_never_consumed():
    # AC-4.2: Characters of the following word are never consumed
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # "X" intact

def test_wrap_text_tab_indentation_preserved():
    # AC-4.3: Tab indentation at the start of a segment after a line break is preserved
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # tab preserved

def test_wrap_text_no_breaks_at_leading_space():
    # AC-4.4: A line that starts with a space does not break at that space
    assert wrap_text(" hello", 3) == " he\nllo"  # breaks at width