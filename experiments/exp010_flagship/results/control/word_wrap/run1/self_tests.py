from solution import wrap_text

def test_wrap_text_fits_within_width():
    # AC-1.1: "abcde" fits within width 5
    assert wrap_text("abcde", 5) == ["abcde"]  
    # AC-1.1: "ab cd" at width 5 stays one line
    assert wrap_text("ab cd", 5) == ["ab cd"]  

def test_wrap_text_exceeds_width():
    # AC-1.2: "Let's  Go" at width 5 becomes ["Let's", "Go"]
    assert wrap_text("Let's  Go", 5) == ["Let's", "Go"]  
    # AC-1.2: "Lets go outside now" at width 7 becomes ["Lets go", "outside", "now"]
    assert wrap_text("Lets go outside now", 7) == ["Lets go", "outside", "now"]  
    # AC-1.3: "extraordinary" at width 5 becomes ["extra", "ordin", "ary"]
    assert wrap_text("extraordinary", 5) == ["extra", "ordin", "ary"]  
    # AC-1.4: "a bcdef" at width 5 becomes ["a", "bcdef"]
    assert wrap_text("a bcdef", 5) == ["a", "bcdef"]  
    # AC-1.5: "aaa bb" at width 3 becomes ["aaa", "bb"]
    assert wrap_text("aaa bb", 3) == ["aaa", "bb"]  

def test_wrap_text_missing_or_blank_input():
    # AC-2.1: No text returns empty string
    assert wrap_text("", 5) == []  
    # AC-2.2: Whitespace-only text returns empty string
    assert wrap_text(" ", 5) == []  
    assert wrap_text("\t", 5) == []  
    # AC-2.3: "hi  " at width 2 becomes just ["hi"]
    assert wrap_text("hi  ", 2) == ["hi"]  

def test_wrap_text_respects_line_breaks():
    # AC-3.1: breaks at line breaks
    assert wrap_text("\nLet's Go\noutside.", 5) == ["", "Let's", "Go", "outside."]  
    # AC-3.2: consecutive line breaks preserved
    assert wrap_text("\n\nLet's Go\noutside.", 5) == ["", "", "Let's", "Go", "outside."]  
    # AC-3.3: column counting restarts after line break
    assert wrap_text("abc\ndef", 4) == ["abc", "def"]  
    # AC-3.4: segments around existing breaks that fit within width stay unchanged
    assert wrap_text("ab\ncd", 2) == ["ab", "cd"]  

def test_wrap_text_consumes_only_spaces_at_breaks():
    # AC-4.1: "ab \tcd" at width 3 becomes ["ab", "\tcd"]
    assert wrap_text("ab \tcd", 3) == ["ab", "\tcd"]  
    # AC-4.2: "ab Xcd" at width 3 becomes ["ab", "Xcd"]
    assert wrap_text("ab Xcd", 3) == ["ab", "Xcd"]  
    # AC-4.3: tab indentation preserved
    assert wrap_text("ab\n\tcd", 10) == ["ab", "\tcd"]  
    # AC-4.4: " hello" at width 3 becomes [" he", "llo"]
    assert wrap_text(" hello", 3) == [" he", "llo"]