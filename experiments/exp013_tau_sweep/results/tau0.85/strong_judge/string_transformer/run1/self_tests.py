from solution import text_styling_pipeline

# US-1: Capitalise words
def test_capitalise_words():
    assert text_styling_pipeline("hello world").capitalise() == "Hello World"  # AC-1.1
    assert text_styling_pipeline("hello WORLD").capitalise() == "Hello WORLD"  # AC-1.2
    assert text_styling_pipeline("").capitalise() == ""  # AC-1.3
    assert text_styling_pipeline("teXas rocks").capitalise() == "TeXas Rocks"  # AC-1.4

# US-2: Reverse text and strip whitespace
def test_reverse_text():
    assert text_styling_pipeline("hello world").reverse() == "dlrow olleh"  # AC-2.1

def test_strip_whitespace():
    assert text_styling_pipeline("hello world").strip_whitespace() == "helloworld"  # AC-2.2
    assert text_styling_pipeline("hello \t world\n").strip_whitespace() == "helloworld"  # AC-2.3

# US-3: Restyle into identifier conventions
def test_snake_case():
    assert text_styling_pipeline("hello world").to_snake_case() == "hello_world"  # AC-3.1
    assert text_styling_pipeline("hello-world test").to_snake_case() == "hello_world_test"  # AC-3.2
    assert text_styling_pipeline("Hello World").to_snake_case() == "hello_world"  # AC-3.3

def test_camel_case():
    assert text_styling_pipeline("Hello World").to_camel_case() == "helloWorld"  # AC-3.4
    assert text_styling_pipeline("one two three").to_camel_case() == "oneTwoThree"  # AC-3.4
    assert text_styling_pipeline("HELLO WORLD").to_camel_case() == "helloWorld"  # AC-3.5
    assert text_styling_pipeline("singleword").to_camel_case() == "singleword"  # AC-3.6
    assert text_styling_pipeline("").to_camel_case() == ""  # AC-3.7
    assert text_styling_pipeline("   ").to_camel_case() == ""  # AC-3.7

# US-4: Truncate and repeat
def test_truncate():
    assert text_styling_pipeline("hello world").truncate(5) == "hello…"  # AC-4.1
    assert text_styling_pipeline("hello").truncate(5) == "hello"  # AC-4.2
    assert text_styling_pipeline("hello").truncate(6) == "hello"  # AC-4.2
    assert text_styling_pipeline("hello").truncate(0) == "…"  # AC-4.3
    try:
        text_styling_pipeline("hello").truncate(-1)  # AC-4.4 -- expect refusal
    except ValueError as e:
        assert str(e) == "length must not be negative"  # Check refusal message

def test_repeat():
    assert text_styling_pipeline("ha").repeat(3) == "ha ha ha"  # AC-4.5
    assert text_styling_pipeline("ha").repeat(1) == "ha"  # AC-4.6
    assert text_styling_pipeline("ha").repeat(0) == ""  # AC-4.6
    try:
        text_styling_pipeline("ha").repeat(-1)  # AC-4.7 -- expect refusal
    except ValueError as e:
        assert str(e) == "times must not be negative"  # Check refusal message

# US-5: Replace text and chain transformations
def test_replace():
    assert text_styling_pipeline("hello world hello").replace("hello", "bye") == "bye world bye"  # AC-5.1

def test_chain_transformations():
    assert text_styling_pipeline("hello world").capitalise().to_snake_case().truncate(5) == "hello…"  # AC-5.2
    assert text_styling_pipeline("hello world").reverse().capitalise() == "Dlrow Olleh"  # Check reverse then capitalise
    assert text_styling_pipeline("hello world").capitalise().reverse() == "dlroW olleH"  # Check capitalise then reverse

def test_no_transformations():
    assert text_styling_pipeline("unchanged") == "unchanged"  # AC-5.3