from solution import justify_text

def test_single_word_within_width():
    # "Hello" fits within width 5 unchanged.
    assert justify_text("Hello", 5) == ["Hello"]

def test_single_word_exactly_width():
    # "Hello" fits exactly in width 5.
    assert justify_text("Hello", 5) == ["Hello"]

def test_multiple_words_fit_in_one_line():
    # "This is" fits within width 8, so it stays unchanged.
    assert justify_text("This is", 8) == ["This is"]

def test_words_packed_greedily():
    # "This is an" at width 10 yields "This is an".
    # The next word "example" flows to the next line.
    assert justify_text("This is an example", 10) == ["This is an", "example"]

def test_last_line_flush_left():
    # "This is an example of text justification." at width 16.
    # The last line is flush left: "justification."
    assert justify_text("This is an example of text justification.", 16) == ["This    is    an", "example  of text", "justification."]

def test_oversized_word_on_own_line():
    # "oversized" is longer than width 5, so it overflows.
    assert justify_text("oversized", 5) == ["oversized"]

def test_tolerate_messy_spacing():
    # Multiple spaces and tabs should count as a single separator.
    assert justify_text("This   is\tan example", 10) == ["This is an", "example"]

def test_empty_or_whitespace_text():
    # Whitespace-only text produces no lines at all.
    assert justify_text("   \t \n", 10) == []

def test_single_word_shorter_than_width():
    # "Hi" fits within width 5 unchanged.
    assert justify_text("Hi", 5) == ["Hi"]

def test_width_one():
    # Each word fits in its own line at width 1.
    assert justify_text("a b c", 1) == ["a", "b", "c"]

def test_words_exactly_fill_later_non_final_line():
    # "a b c d e" at width 3 yields "a b", "c d", "e".
    assert justify_text("a b c d e", 3) == ["a b", "c d", "e"]

def test_non_final_single_word_line_right_padding():
    # "a long bb" at width 5 yields "a    ", "long ", "bb".
    assert justify_text("a long bb", 5) == ["a    ", "long ", "bb"]

def test_oversized_word_among_others():
    # "a oversized b" at width 5 yields "a    ", "oversized", "b".
    assert justify_text("a oversized b", 5) == ["a    ", "oversized", "b"]

def test_line_breaks_separate_words():
    # "a\nb" at width 3 yields "a b".
    assert justify_text("a\nb", 3) == ["a b"]

def test_empty_string_input():
    # An empty string should produce no lines.
    assert justify_text("", 10) == []