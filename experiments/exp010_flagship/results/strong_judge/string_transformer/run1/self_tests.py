from solution import chainable_text_styling_pipeline
import pytest

def test_capitalise_words():
    assert chainable_text_styling_pipeline("hello world").capitalise_words() == "Hello World"  # AC-1.1
    assert chainable_text_styling_pipeline("hello WORLD").capitalise_words() == "Hello WORLD"  # AC-1.2
    assert chainable_text_styling_pipeline("").capitalise_words() == ""  # AC-1.3
    assert chainable_text_styling_pipeline("teXas rocks").capitalise_words() == "TeXas Rocks"  # AC-1.4

def test_reverse_text_and_strip_whitespace():
    assert chainable_text_styling_pipeline("hello world").reverse() == "dlrow olleh"  # AC-2.1
    assert chainable_text_styling_pipeline("hello world").strip_whitespace() == "helloworld"  # AC-2.2
    assert chainable_text_styling_pipeline("hello \t world\n").strip_whitespace() == "helloworld"  # AC-2.3

def test_restyle_into_identifier_conventions():
    assert chainable_text_styling_pipeline("hello world").to_snake_case() == "hello_world"  # AC-3.1
    assert chainable_text_styling_pipeline("hello-world test").to_snake_case() == "hello_world_test"  # AC-3.2
    assert chainable_text_styling_pipeline("Hello World").to_snake_case() == "hello_world"  # AC-3.3
    assert chainable_text_styling_pipeline("Hello World").to_camel_case() == "helloWorld"  # AC-3.4
    assert chainable_text_styling_pipeline("HELLO WORLD").to_camel_case() == "helloWorld"  # AC-3.5
    assert chainable_text_styling_pipeline("singleword").to_camel_case() == "singleword"  # AC-3.6
    assert chainable_text_styling_pipeline("   ").to_camel_case() == ""  # AC-3.7
    assert chainable_text_styling_pipeline("").to_camel_case() == ""  # AC-3.7 (empty input)
    assert chainable_text_styling_pipeline("one two three").to_camel_case() == "oneTwoThree"  # AC-3.4 (multiple words)

def test_truncate_and_repeat():
    assert chainable_text_styling_pipeline("hello world").truncate(5) == "hello…"  # AC-4.1
    assert chainable_text_styling_pipeline("hello").truncate(10) == "hello"  # AC-4.2 (beyond text length)
    assert chainable_text_styling_pipeline("hello").truncate(5) == "hello"  # AC-4.2 (exact length)
    assert chainable_text_styling_pipeline("hello").truncate(0) == "…"  # AC-4.3
    assert chainable_text_styling_pipeline("ha").repeat(3) == "ha ha ha"  # AC-4.5
    assert chainable_text_styling_pipeline("ha").repeat(1) == "ha"  # AC-4.6
    assert chainable_text_styling_pipeline("ha").repeat(0) == ""  # AC-4.6 (repeat zero)

def test_replace_text_and_chain_transformations():
    assert chainable_text_styling_pipeline("hello world hello").replace("hello", "bye") == "bye world bye"  # AC-5.1
    assert chainable_text_styling_pipeline("hello world").capitalise_words().strip_whitespace() == "Helloworld"  # AC-5.2 (order sensitivity)
    assert chainable_text_styling_pipeline("hello world").strip_whitespace().capitalise_words() == "Helloworld"  # AC-5.2 (order sensitivity)
    assert chainable_text_styling_pipeline("no transformations").apply() == "no transformations"  # AC-5.3