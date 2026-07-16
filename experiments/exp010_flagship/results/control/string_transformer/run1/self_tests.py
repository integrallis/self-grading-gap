from solution import TextStyler

def test_capitalise_words_basic():
    assert TextStyler("hello world").capitalise_words() == "Hello World"  # First letter uppercased

def test_capitalise_words_mixed_case():
    assert TextStyler("hello WORLD").capitalise_words() == "Hello WORLD"  # Other letters untouched

def test_capitalise_words_empty():
    assert TextStyler("").capitalise_words() == ""  # Capitalising empty text yields empty text

def test_capitalise_words_with_separators():
    assert TextStyler("teXas rocks").capitalise_words() == "TeXas Rocks"  # Uppercase inside word does not start new word

def test_reverse_text_basic():
    assert TextStyler("hello world").reverse() == "dlrow olleh"  # Whole text reversed

def test_strip_whitespace_basic():
    assert TextStyler("hello world").strip_whitespace() == "helloworld"  # Spaces removed

def test_strip_whitespace_tabs_and_newlines():
    assert TextStyler("hello \t world\n").strip_whitespace() == "helloworld"  # Tabs and newlines removed

def test_snake_case_basic():
    assert TextStyler("hello world").to_snake_case() == "hello_world"  # Words joined with underscores

def test_snake_case_with_hyphens():
    assert TextStyler("hello-world test").to_snake_case() == "hello_world_test"  # Hyphens as separators

def test_snake_case_lowercase():
    assert TextStyler("Hello World").to_snake_case() == "hello_world"  # Lowercases every word

def test_camel_case_basic():
    assert TextStyler("Hello World").to_camel_case() == "helloWorld"  # Camel case normalisation

def test_camel_case_with_uppercase():
    assert TextStyler("HELLO WORLD").to_camel_case() == "helloWorld"  # Normalises fully uppercase input

def test_camel_case_single_word():
    assert TextStyler("hello").to_camel_case() == "hello"  # Single word lowercased

def test_camel_case_empty_or_only_separators():
    assert TextStyler("").to_camel_case() == ""  # Empty text yields empty text
    assert TextStyler("  ").to_camel_case() == ""  # Only separators yield empty text

def test_truncate_basic():
    assert TextStyler("hello world").truncate(5) == "hello…"  # Cuts to requested length with ellipsis

def test_truncate_no_change():
    assert TextStyler("hello").truncate(10) == "hello"  # Length equal or beyond leaves unchanged

def test_truncate_zero_length():
    assert TextStyler("hello").truncate(0) == "…"  # Truncating to zero removes everything

def test_truncate_negative_length():
    try:
        TextStyler("hello").truncate(-1)
    except ValueError as e:
        assert str(e) == "length must not be negative"  # Negative length refusal

def test_repeat_basic():
    assert TextStyler("ha").repeat(3) == "ha ha ha"  # Repeat text with spaces

def test_repeat_once():
    assert TextStyler("ha").repeat(1) == "ha"  # Repeating once leaves unchanged

def test_repeat_zero():
    assert TextStyler("ha").repeat(0) == ""  # Repeating zero times yields empty text

def test_repeat_negative():
    try:
        TextStyler("ha").repeat(-1)
    except ValueError as e:
        assert str(e) == "times must not be negative"  # Negative repeat count refusal

def test_replace_basic():
    assert TextStyler("hello world hello").replace("hello", "bye") == "bye world bye"  # Replacement of text

def test_chain_transformations():
    assert TextStyler("hello world").capitalise_words().reverse() == "dlroW olleH"  # Chained transformations
    assert TextStyler("hello world").strip_whitespace().to_snake_case() == "helloworld"  # Chained transformations

def test_no_transformations():
    assert TextStyler("hello world").no_transformations() == "hello world"  # No transformations yields original text