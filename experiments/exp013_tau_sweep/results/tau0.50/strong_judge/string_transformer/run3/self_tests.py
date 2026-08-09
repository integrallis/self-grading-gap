import pytest
from solution import chainable_text_styling_pipeline

# US-1: Capitalise words
def test_capitalise_words():
    assert chainable_text_styling_pipeline("hello world").capitalise() == "Hello World"  # AC-1.1
    assert chainable_text_styling_pipeline("hello WORLD").capitalise() == "Hello WORLD"  # AC-1.2
    assert chainable_text_styling_pipeline("").capitalise() == ""  # AC-1.3
    assert chainable_text_styling_pipeline("teXas rocks").capitalise() == "TeXas Rocks"  # AC-1.4

# US-2: Reverse text and strip whitespace
def test_reverse_text():
    assert chainable_text_styling_pipeline("hello world").reverse() == "dlrow olleh"  # AC-2.1

def test_strip_whitespace():
    assert chainable_text_styling_pipeline("hello world").strip_whitespace() == "helloworld"  # AC-2.2
    assert chainable_text_styling_pipeline("hello\tworld\n").strip_whitespace() == "helloworld"  # AC-2.3

# US-3: Restyle into identifier conventions
def test_snake_case():
    assert chainable_text_styling_pipeline("hello world").to_snake_case() == "hello_world"  # AC-3.1
    assert chainable_text_styling_pipeline("hello-world test").to_snake_case() == "hello_world_test"  # AC-3.2
    assert chainable_text_styling_pipeline("Hello World").to_snake_case() == "hello_world"  # AC-3.3

def test_camel_case():
    assert chainable_text_styling_pipeline("Hello World").to_camel_case() == "helloWorld"  # AC-3.4
    assert chainable_text_styling_pipeline("HELLO WORLD").to_camel_case() == "helloWorld"  # AC-3.5
    assert chainable_text_styling_pipeline("one two three").to_camel_case() == "oneTwoThree"  # AC-3.4
    assert chainable_text_styling_pipeline("single").to_camel_case() == "single"  # AC-3.6
    assert chainable_text_styling_pipeline("").to_camel_case() == ""  # AC-3.7
    assert chainable_text_styling_pipeline("   ").to_camel_case() == ""  # AC-3.7 separators-only

# US-4: Truncate and repeat
def test_truncate():
    assert chainable_text_styling_pipeline("hello world").truncate(5) == "hello…"  # AC-4.1
    assert chainable_text_styling_pipeline("hello").truncate(5) == "hello"  # AC-4.2
    assert chainable_text_styling_pipeline("hello").truncate(6) == "hello"  # AC-4.2 beyond length
    assert chainable_text_styling_pipeline("hello").truncate(0) == "…"  # AC-4.3
    assert chainable_text_styling_pipeline("hello").truncate(-1) == "length must not be negative"  # AC-4.4

def test_repeat():
    assert chainable_text_styling_pipeline("ha").repeat(3) == "ha ha ha"  # AC-4.5
    assert chainable_text_styling_pipeline("ha").repeat(1) == "ha"  # AC-4.6
    assert chainable_text_styling_pipeline("ha").repeat(0) == ""  # AC-4.6
    assert chainable_text_styling_pipeline("ha").repeat(-1) == "times must not be negative"  # AC-4.7

# US-5: Replace text and chain transformations
def test_replace():
    assert chainable_text_styling_pipeline("hello world hello").replace("hello", "bye") == "bye world bye"  # AC-5.1

def test_chain_transformations():
    assert chainable_text_styling_pipeline("hello world").capitalise().reverse() == "dlroW olleH"  # AC-5.2 opposite order
    assert chainable_text_styling_pipeline("hello world").reverse().capitalise() == "Dlrow Olleh"  # AC-5.2 opposite order
    assert chainable_text_styling_pipeline("unchanged") == "unchanged"  # AC-5.3 no transformations requested