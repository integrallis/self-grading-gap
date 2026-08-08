from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: Input text fits within the width.
    assert wrap_text("ab cd", 5) == "ab cd"  # text is exactly at width
    assert wrap_text("hello", 6) == "hello"  # text is less than width

def test_wrap_text_exceeds_width():
    # AC-1.2: Break at the last space that fits within the width.
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # break at last space
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # multiple breaks

    # AC-1.3: Hard split for long words.
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # hard split

    # AC-1.4: One-letter first word still breaks at space.
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # space consumed

    # AC-1.5: Column counting restarts after break.
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # reset counting after break

def test_wrap_text_missing_or_blank_input():
    # AC-2.1: No text provided.
    assert wrap_text("", 5) == ""  # empty input returns empty string

    # AC-2.2: Whitespace-only text produces empty result.
    assert wrap_text(" ", 5) == ""  # single space
    assert wrap_text("\t", 5) == ""  # single tab

    # AC-2.3: Trailing spaces are dropped.
    assert wrap_text("hi  ", 2) == "hi"  # trailing spaces dropped

def test_wrap_text_respects_line_breaks():
    # AC-3.1: Existing line breaks are kept, wrapping independently.
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # breaks independently

    # AC-3.2: Consecutive line breaks preserved.
    assert wrap_text("\n\nhello\nworld", 5) == "\n\nhello\nworld"  # multiple breaks intact

    # AC-3.3: Column counting restarts after a line break.
    assert wrap_text("abc\nxyz", 4) == "abc\nxyz"  # independent segments

    # AC-3.4: Segments around existing breaks that fit stay unchanged.
    assert wrap_text("hi\nthere", 5) == "hi\nthere"  # both fit

def test_wrap_text_consumes_only_spaces():
    # AC-4.1: Only spaces consumed at a break.
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # tab survives

    # AC-4.2: Characters of the following word are not consumed.
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # "X" intact

    # AC-4.3: Tab indentation preserved after line break.
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # tab remains

    # AC-4.4: Line starts with a space does not break at that space.
    assert wrap_text(" hello", 3) == " he\nllo"  # hard break at width