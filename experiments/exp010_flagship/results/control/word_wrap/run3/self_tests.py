from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: Text that already fits within the width is returned unchanged
    assert wrap_text("ab cd", 5) == ["ab cd"]  # fits exactly within width
    assert wrap_text("hello", 5) == ["hello"]  # fits within width

def test_wrap_text_breaks_at_last_space():
    # AC-1.2: Break at the last space that fits within the width
    assert wrap_text("Let's  Go", 5) == ["Let's", "Go"]  # breaks at space
    assert wrap_text("Lets go outside now", 7) == ["Lets go", "outside", "now"]  # breaks at spaces

def test_wrap_text_hard_splits_long_words():
    # AC-1.3: A single word longer than the width is hard-split at the width
    assert wrap_text("extraordinary", 5) == ["extra", "ordin", "ary"]  # hard splits

def test_wrap_text_breaks_first_word_space():
    # AC-1.4: A one-letter first word still breaks at its space
    assert wrap_text("a bcdef", 5) == ["a", "bcdef"]  # breaks at space

def test_wrap_text_column_count_resets_after_break():
    # AC-1.5: Column counting restarts after an inserted break
    assert wrap_text("aaa bb", 3) == ["aaa", "bb"]  # no further break after reset

def test_wrap_text_empty_input():
    # AC-2.1: When no text is provided, the result is the empty string
    assert wrap_text("", 5) == []  # empty input

def test_wrap_text_whitespace_only_input():
    # AC-2.2: Whitespace-only text produces the empty string
    assert wrap_text(" ", 5) == []  # single space
    assert wrap_text("\t", 5) == []  # single tab

def test_wrap_text_trailing_spaces_dropped():
    # AC-2.3: Trailing spaces beyond the width are dropped
    assert wrap_text("hi  ", 2) == ["hi"]  # drops trailing spaces

def test_wrap_text_respects_existing_line_breaks():
    # AC-3.1: Existing line breaks are kept
    assert wrap_text("\nLet's Go\noutside.", 5) == ["", "Let's", "Go", "outside."]  # preserves breaks

def test_wrap_text_preserves_consecutive_line_breaks():
    # AC-3.2: Consecutive line breaks are preserved
    assert wrap_text("\n\nhello\n\n", 5) == ["", "", "hello", "", ""]  # preserves consecutive breaks

def test_wrap_text_column_count_resets_after_line_break():
    # AC-3.3: Column counting restarts after an existing line break
    assert wrap_text("abc\ndefg", 4) == ["abc", "defg"]  # counting restarts after break

def test_wrap_text_segments_fit_within_width():
    # AC-3.4: Segments around an existing break that fit within the width stay the same
    assert wrap_text("abc\ndef", 3) == ["abc", "def"]  # segments fit

def test_wrap_text_consume_only_spaces_at_breaks():
    # AC-4.1: Only spaces are consumed at a break
    assert wrap_text("ab \tcd", 3) == ["ab", "\tcd"]  # tab survives

def test_wrap_text_characters_not_consumed_at_break():
    # AC-4.2: Characters of the following word are never consumed at a break
    assert wrap_text("ab Xcd", 3) == ["ab", "Xcd"]  # 'X' intact

def test_wrap_text_tab_indentation_preserved():
    # AC-4.3: Tab indentation at the start of a segment after a line break is preserved
    assert wrap_text("ab\n\tcd", 10) == ["ab", "\tcd"]  # tab preserved

def test_wrap_text_no_break_at_start_space():
    # AC-4.4: A line that starts with a space does not break at that space
    assert wrap_text(" hello", 3) == [" he", "llo"]  # hard break at width