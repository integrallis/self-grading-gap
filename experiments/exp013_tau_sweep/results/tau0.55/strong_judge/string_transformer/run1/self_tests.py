import pytest
from solution import text_styling_pipeline

def test_capitalise_words():
    assert text_styling_pipeline.capitalise_words("hello world") == "Hello World"  # AC-1.1
    assert text_styling_pipeline.capitalise_words("hello WORLD") == "Hello WORLD"  # AC-1.2
    assert text_styling_pipeline.capitalise_words("") == ""  # AC-1.3
    assert text_styling_pipeline.capitalise_words("teXas rocks") == "TeXas Rocks"  # AC-1.4

def test_reverse_text_and_strip_whitespace():
    assert text_styling_pipeline.reverse_text("hello world") == "dlrow olleh"  # AC-2.1
    assert text_styling_pipeline.strip_whitespace("hello world") == "helloworld"  # AC-2.2
    assert text_styling_pipeline.strip_whitespace("hello\tworld\n") == "helloworld"  # AC-2.3

def test_restylers():
    assert text_styling_pipeline.to_snake_case("hello world") == "hello_world"  # AC-3.1
    assert text_styling_pipeline.to_snake_case("hello-world test") == "hello_world_test"  # AC-3.2
    assert text_styling_pipeline.to_snake_case("Hello World") == "hello_world"  # AC-3.3
    assert text_styling_pipeline.to_camel_case("Hello World") == "helloWorld"  # AC-3.4
    assert text_styling_pipeline.to_camel_case("HELLO WORLD") == "helloWorld"  # AC-3.5
    assert text_styling_pipeline.to_camel_case("singleword") == "singleword"  # AC-3.6
    assert text_styling_pipeline.to_camel_case("") == ""  # AC-3.7
    assert text_styling_pipeline.to_camel_case(" \t\n") == ""  # AC-3.7 (separators-only case)

def test_truncate_and_repeat():
    assert text_styling_pipeline.truncate("hello world", 5) == "hello…"  # AC-4.1
    assert text_styling_pipeline.truncate("hello world", 11) == "hello world"  # AC-4.2
    assert text_styling_pipeline.truncate("hello world", 12) == "hello world"  # AC-4.2 (beyond length)
    assert text_styling_pipeline.truncate("hello world", 0) == "…"  # AC-4.3
    assert text_styling_pipeline.truncate("hello world", -1) == "length must not be negative"  # AC-4.4 (refusal message)
    
    assert text_styling_pipeline.repeat("ha", 3) == "ha ha ha"  # AC-4.5
    assert text_styling_pipeline.repeat("ha", 1) == "ha"  # AC-4.6
    assert text_styling_pipeline.repeat("ha", 0) == ""  # AC-4.6
    assert text_styling_pipeline.repeat("ha", -1) == "times must not be negative"  # AC-4.7 (refusal message)

def test_replace_text_and_chain_transformations():
    assert text_styling_pipeline.replace("hello world hello", "hello", "bye") == "bye world bye"  # AC-5.1
    assert text_styling_pipeline.strip_whitespace("hello world").capitalise_words() == "Helloworld"  # AC-5.2 (order difference)
    assert text_styling_pipeline.capitalise_words("hello world").strip_whitespace() == "HelloWorld"  # AC-5.2
    assert text_styling_pipeline.replace("unchanged text", "", "") == "unchanged text"  # AC-5.3 (no transformations)

def test_no_transformations():
    assert text_styling_pipeline.no_transformations("unchanged text") == "unchanged text"  # AC-5.3