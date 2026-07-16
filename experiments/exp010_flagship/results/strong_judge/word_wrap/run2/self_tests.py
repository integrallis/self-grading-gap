def test_wrap_text_fits_width():
    # AC-1.1: Text that already fits within the width is returned unchanged
    assert wrap_text("ab cd", 5) == "ab cd"  # already fits width of 5
    assert wrap_text("hello", 5) == "hello"  # exactly at the width

def test_wrap_text_breaks_at_last_space():
    # AC-1.2: Break at the last space that fits within the width
    assert wrap_text("Let's  Go", 5) == "Let's\nGo"  # breaks at last space
    assert wrap_text("Lets go outside now", 7) == "Lets go\noutside\nnow"  # breaks at last space

def test_wrap_text_hard_split_long_word():
    # AC-1.3: A single word longer than the width is hard-split at the width
    assert wrap_text("extraordinary", 5) == "extra\nordin\nary"  # hard split

def test_wrap_text_one_letter_first_word():
    # AC-1.4: A one-letter first word still breaks at its space
    assert wrap_text("a bcdef", 5) == "a\nbcdef"  # breaks at space

def test_wrap_text_column_count_restarts():
    # AC-1.5: Column counting restarts after an inserted break
    assert wrap_text("aaa bb", 3) == "aaa\nbb"  # breaks at space, counting restarts

def test_wrap_text_empty_and_whitespace_input():
    # AC-2.1: When no text is provided at all, the result is the empty string
    assert wrap_text("", 5) == ""  # empty string
    # AC-2.2: Whitespace-only text produces the empty string
    assert wrap_text(" ", 5) == ""  # whitespace only
    assert wrap_text("\t", 5) == ""  # tab only
    # AC-2.3: Trailing spaces beyond the width are dropped
    assert wrap_text("hi  ", 2) == "hi"  # trailing spaces dropped

def test_wrap_text_respects_line_breaks():
    # AC-3.1: Existing line breaks are kept, text wraps independently
    assert wrap_text("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # preserves breaks
    # AC-3.2: Consecutive line breaks are preserved
    assert wrap_text("\n\nHello World\n", 5) == "\n\nHello\nWorld\n"  # preserves consecutive breaks
    # AC-3.3: Column counting restarts after a line break
    assert wrap_text("abc\nxyz", 4) == "abc\nxyz"  # counting restarts after break
    # AC-3.4: Segments around an existing break that fit within the width stay as they are
    assert wrap_text("abc\ndef", 3) == "abc\ndef"  # both fit within the width

def test_wrap_text_consumes_only_spaces():
    # AC-4.1: Only spaces are consumed at a break
    assert wrap_text("ab \tcd", 3) == "ab\n\tcd"  # tab survives
    # AC-4.2: Characters of the following word are never consumed at a break
    assert wrap_text("ab Xcd", 3) == "ab\nXcd"  # 'X' intact
    # AC-4.3: Tab indentation at the start of a segment after a line break is preserved
    assert wrap_text("ab\n\tcd", 10) == "ab\n\tcd"  # tab intact
    # AC-4.4: A line that starts with a space does not break at that space
    assert wrap_text(" hello", 3) == " he\nllo"  # breaks at width, not space