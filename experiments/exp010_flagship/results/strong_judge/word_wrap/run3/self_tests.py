from solution import text_wrap

def test_wrap_text_that_fits_within_width():
    assert text_wrap("ab cd", 5) == "ab cd"  # AC-1.1
    assert text_wrap("hello", 5) == "hello"  # AC-1.1

def test_wrap_text_broken_at_last_space():
    assert text_wrap("Let's  Go", 5) == "Let's\nGo"  # AC-1.2
    assert text_wrap("Lets go outside now", 7) == "Lets go\noutside\nnow"  # AC-1.2

def test_wrap_single_word_longer_than_width():
    assert text_wrap("extraordinary", 5) == "extra\nordin\nary"  # AC-1.3

def test_wrap_one_letter_first_word():
    assert text_wrap("a bcdef", 5) == "a\nbcdef"  # AC-1.4

def test_wrap_column_count_restarts_after_break():
    assert text_wrap("aaa bb", 3) == "aaa\nbb"  # AC-1.5

def test_handle_missing_text():
    assert text_wrap("", 5) == ""  # AC-2.1
    assert text_wrap(" ", 5) == ""  # AC-2.2
    assert text_wrap("\t", 5) == ""  # AC-2.2

def test_handle_trailing_spaces():
    assert text_wrap("hi  ", 2) == "hi"  # AC-2.3

def test_respect_line_breaks():
    assert text_wrap("\nLet's Go\noutside.", 5) == "\nLet's\nGo\noutsi\nde."  # AC-3.1
    assert text_wrap("\n\nLet's Go\noutside.", 5) == "\n\nLet's\nGo\noutsi\nde."  # AC-3.2
    assert text_wrap("abc\ndef", 4) == "abc\ndef"  # AC-3.3
    assert text_wrap("abc\ndef", 6) == "abc\ndef"  # AC-3.4

def test_consume_only_spaces_at_breaks():
    assert text_wrap("ab \tcd", 3) == "ab\n\tcd"  # AC-4.1
    assert text_wrap("ab Xcd", 3) == "ab\nXcd"  # AC-4.2
    assert text_wrap("ab\n\tcd", 10) == "ab\n\tcd"  # AC-4.3
    assert text_wrap(" hello", 3) == " he\nllo"  # AC-4.4