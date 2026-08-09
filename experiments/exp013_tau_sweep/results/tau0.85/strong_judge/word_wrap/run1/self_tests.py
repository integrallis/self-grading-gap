from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: Text that already fits within the width is returned unchanged
    assert wrap_text("ab cd", 5) == "ab cd"  # exactly at width
    assert wrap_text("Hello", 5) == "Hello"  # fits within width

def test_wrap_text_exceeds_width():
    # AC-1.2: Breaks at the last space that fits within the width
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # breaks at last space
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # breaks at spaces

def test_wrap_text_hard_split():
    # AC-1.3: A single word longer than the width is hard-split
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # hard split at width

def test_wrap_text_single_letter_word():
    # AC-1.4: A one-letter first word still breaks at its space
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # breaks at space

def test_wrap_text_column_count_restarts():
    # AC-1.5: Column counting restarts after an inserted break
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # no further break

def test_wrap_text_empty_and_whitespace_input():
    # AC-2.1: When no text is provided at all, the result is the empty string
    assert wrap_text("", 5) == ""  # empty input
    
    # AC-2.2: Whitespace-only text produces the empty string
    assert wrap_text(" ", 5) == ""  # single space
    assert wrap_text("\t", 5) == ""  # single tab

    # AC-2.3: Trailing spaces beyond the width are dropped
    assert wrap_text("hi  ", 2) == "hi"  # trailing spaces dropped

def test_wrap_text_respects_line_breaks():
    # AC-3.1: Existing line breaks are kept and wrapped independently
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # breaks independently

    # AC-3.2: Consecutive line breaks are preserved
    assert wrap_text("\n\nLet's Go\noutside.", 5) == "\n\nLet's\nGo\noutsi\nde."  # consecutive breaks

    # AC-3.3: Column counting restarts after an existing line break
    assert wrap_text("abc\nabc\nabc", 4) == "abc\nabc\nabc"  # fits around breaks

    # AC-3.4: Segments around existing breaks that fit within the width stay unchanged
    assert wrap_text("abc\nab\nabc", 4) == "abc\nab\nabc"  # segments fit

def test_wrap_text_space_consumption():
    # AC-4.1: Only spaces are consumed at a break
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # tab survives

    # AC-4.2: Characters of the following word are never consumed at a break
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # 'X' intact

    # AC-4.3: Tab indentation at the start of a segment after a line break is preserved
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # tab preserved

    # AC-4.4: A line that starts with a space does not break at that space
    assert wrap_text(" hello", 3) == " he\nllo"  # hard break at width