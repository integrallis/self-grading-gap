from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1
    assert wrap_text("ab cd", 5) == "ab cd"  # Text fits, return unchanged
    # AC-1.1
    assert wrap_text("abcde", 5) == "abcde"  # Text fits, return unchanged
    # AC-1.3
    assert wrap_text("abcde", 4) == "abcd\ne"  # Hard split on long word

def test_wrap_text_breaks_at_spaces():
    # AC-1.2
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # Breaks at last space
    # AC-1.2
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # Multiple breaks

def test_wrap_text_hard_split():
    # AC-1.3
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # Hard split on long word
    # AC-1.4
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # One-letter first word still breaks at space

def test_wrap_text_column_count_restarts():
    # AC-1.5
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # Column counting restarts after break

def test_wrap_text_handles_missing_and_blank_input():
    # AC-2.1
    assert wrap_text("", 5) == ""  # Empty input
    # AC-2.2
    assert wrap_text(" ", 5) == ""  # Whitespace-only input
    assert wrap_text("\t", 5) == ""  # Whitespace-only input
    # AC-2.3
    assert wrap_text("hi  ", 2) == "hi"  # Trailing spaces dropped

def test_wrap_text_respects_line_breaks():
    # AC-3.1
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # Breaks independently
    # AC-3.2
    assert wrap_text("\n\n", 5) == "\n\n"  # Consecutive line breaks preserved
    # AC-3.3
    assert wrap_text("abc\nabc", 4) == "abc\nabc"  # Column counting restarts after break
    # AC-3.4
    assert wrap_text("abc\nabcd", 4) == "abc\nabcd"  # Fits within width stay unchanged

def test_wrap_text_consume_only_spaces():
    # AC-4.1
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # Tab survives
    # AC-4.2
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # Character not consumed
    # AC-4.3
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # Tab preserved after break
    # AC-4.4
    assert wrap_text(" hello", 3) == " he\nllo"  # Hard-break at width, not at space