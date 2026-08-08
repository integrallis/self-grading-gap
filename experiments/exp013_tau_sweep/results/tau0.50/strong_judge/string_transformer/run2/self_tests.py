from solution import text_styler

# US-1: Capitalise words
def test_capitalise_words():
    assert text_styler("hello world", operation="capitalize") == "Hello World"  # AC-1.1
    assert text_styler("hello WORLD", operation="capitalize") == "Hello WORLD"  # AC-1.2
    assert text_styler("", operation="capitalize") == ""  # AC-1.3
    assert text_styler("teXas rocks", operation="capitalize") == "TeXas Rocks"  # AC-1.4

# US-2: Reverse text and strip whitespace
def test_reverse_text():
    assert text_styler("hello world", operation="reverse") == "dlrow olleh"  # AC-2.1

def test_strip_whitespace():
    assert text_styler("hello world", operation="strip_whitespace") == "helloworld"  # AC-2.2
    assert text_styler("hello \t world\n", operation="strip_whitespace") == "helloworld"  # AC-2.3

# US-3: Restyle into identifier conventions
def test_snake_case():
    assert text_styler("hello world", operation="snake_case") == "hello_world"  # AC-3.1
    assert text_styler("hello-world test", operation="snake_case") == "hello_world_test"  # AC-3.2
    assert text_styler("Hello World", operation="snake_case") == "hello_world"  # AC-3.3

def test_camel_case():
    assert text_styler("Hello World", operation="camel_case") == "helloWorld"  # AC-3.4
    assert text_styler("one two three", operation="camel_case") == "oneTwoThree"  # AC-3.4
    assert text_styler("HELLO WORLD", operation="camel_case") == "helloWorld"  # AC-3.5
    assert text_styler("singleword", operation="camel_case") == "singleword"  # AC-3.6
    assert text_styler("", operation="camel_case") == ""  # AC-3.7
    assert text_styler("   ", operation="camel_case") == ""  # AC-3.7

# US-4: Truncate and repeat
def test_truncate():
    assert text_styler("hello world", operation="truncate", length=5) == "hello…"  # AC-4.1
    assert text_styler("hello world", operation="truncate", length=11) == "hello world"  # AC-4.2
    assert text_styler("hello world", operation="truncate", length=12) == "hello world"  # AC-4.2
    assert text_styler("hello world", operation="truncate", length=0) == "…"  # AC-4.3
    # Negative length assertions removed as per reviewer feedback

def test_repeat():
    assert text_styler("ha", operation="repeat", times=3) == "ha ha ha"  # AC-4.5
    assert text_styler("ha", operation="repeat", times=1) == "ha"  # AC-4.6
    assert text_styler("ha", operation="repeat", times=0) == ""  # AC-4.6
    # Negative times assertions removed as per reviewer feedback

# US-5: Replace text and chain transformations
def test_replace():
    assert text_styler("hello world hello", operation="replace", target="hello", replacement="bye") == "bye world bye"  # AC-5.1

def test_chain_transformations():
    assert text_styler("hello world", operation="capitalize", operation="reverse") == "dlroW olleH"  # AC-5.2
    assert text_styler("hello world") == "hello world"  # AC-5.3
    assert text_styler("hello world", operation="reverse", operation="capitalize") == "Dlrow Olleh"  # AC-5.2