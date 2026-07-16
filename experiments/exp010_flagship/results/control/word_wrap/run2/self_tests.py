from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: "ab cd" at width 5 stays one line.
    assert wrap_text("ab cd", 5) == ["ab cd"]
    
    # AC-1.1: "abc" at width 5 stays one line.
    assert wrap_text("abc", 5) == ["abc"]
    
    # AC-1.1: "abcde" at width 5 stays one line.
    assert wrap_text("abcde", 5) == ["abcde"]

def test_wrap_text_breaks_at_last_space():
    # AC-1.2: "Let's  Go" at width 5 becomes "Let's" and "Go".
    assert wrap_text("Let's  Go", 5) == ["Let's", "Go"]
    
    # AC-1.2: "Lets go outside now" at width 7 becomes "Lets go", "outside", "now".
    assert wrap_text("Lets go outside now", 7) == ["Lets go", "outside", "now"]

def test_wrap_text_hard_split_long_words():
    # AC-1.3: "extraordinary" at width 5 becomes "extra", "ordin", "ary".
    assert wrap_text("extraordinary", 5) == ["extra", "ordin", "ary"]

def test_wrap_text_one_letter_word():
    # AC-1.4: "a bcdef" at width 5 becomes "a" and "bcdef".
    assert wrap_text("a bcdef", 5) == ["a", "bcdef"]

def test_wrap_text_column_count_restarts():
    # AC-1.5: "aaa bb" at width 3 becomes "aaa" and "bb".
    assert wrap_text("aaa bb", 3) == ["aaa", "bb"]

def test_wrap_text_empty_input():
    # AC-2.1: Empty input returns empty.
    assert wrap_text("", 5) == []
    
    # AC-2.1: None input returns empty.
    assert wrap_text(None, 5) == []

def test_wrap_text_whitespace_only_input():
    # AC-2.2: Single space produces empty string.
    assert wrap_text(" ", 5) == []
    
    # AC-2.2: Single tab produces empty string.
    assert wrap_text("\t", 5) == []

def test_wrap_text_trailing_spaces():
    # AC-2.3: "hi  " at width 2 becomes just "hi".
    assert wrap_text("hi  ", 2) == ["hi"]

def test_wrap_text_respects_line_breaks():
    # AC-3.1: Keeps line breaks and wraps independently.
    assert wrap_text("\nLet's Go\noutside.", 5) == ["", "Let's", "Go", "outsi", "de."]

    # AC-3.2: Consecutive line breaks are preserved.
    assert wrap_text("\n\nLet's Go\n\noutside.", 5) == ["", "", "Let's", "Go", "", "", "outsi", "de."]

    # AC-3.3: Column counting restarts after a line break.
    assert wrap_text("abc\ndefg\nhij", 4) == ["abc", "defg", "hij"]

    # AC-3.4: Segments around an existing break that fit within the width stay the same.
    assert wrap_text("abc\ndef", 4) == ["abc", "def"]

def test_wrap_text_consumes_only_spaces():
    # AC-4.1: "ab \tcd" at width 3 becomes "ab" and "\tcd".
    assert wrap_text("ab \tcd", 3) == ["ab", "\tcd"]
    
    # AC-4.2: "ab Xcd" at width 3 becomes "ab" and "Xcd".
    assert wrap_text("ab Xcd", 3) == ["ab", "Xcd"]

    # AC-4.3: Tab indentation at start of segment after break is preserved.
    assert wrap_text("ab\n\tcd", 10) == ["ab", "\tcd"]

    # AC-4.4: " hello" at width 3 becomes " he" and "llo".
    assert wrap_text(" hello", 3) == [" he", "llo"]