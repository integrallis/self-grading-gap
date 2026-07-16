import pytest
from solution import your_function_name  # replace with the actual function name

def test_capitalise_words():
    assert your_function_name("hello world", transformation='capitalize') == "Hello World"  # AC-1.1
    assert your_function_name("hello WORLD", transformation='capitalize') == "Hello WORLD"  # AC-1.2
    assert your_function_name("hello WORLD", transformation='capitalize') == "Hello WORLD"  # AC-1.2
    assert your_function_name("", transformation='capitalize') == ""  # AC-1.3 (testing empty text)
    assert your_function_name("teXas rocks", transformation='capitalize') == "TeXas Rocks"  # AC-1.4

def test_reverse_and_strip_whitespace():
    assert your_function_name("hello world", transformation='reverse') == "dlrow olleh"  # AC-2.1
    assert your_function_name("hello world", transformation='strip_whitespace') == "helloworld"  # AC-2.2
    assert your_function_name("hello \t world\n", transformation='strip_whitespace') == "helloworld"  # AC-2.3

def test_restyl_into_identifier_conventions():
    assert your_function_name("hello world", transformation='snake_case') == "hello_world"  # AC-3.1
    assert your_function_name("hello-world test", transformation='snake_case') == "hello_world_test"  # AC-3.2
    assert your_function_name("Hello World", transformation='snake_case') == "hello_world"  # AC-3.3
    assert your_function_name("Hello World", transformation='camel_case') == "helloWorld"  # AC-3.4
    assert your_function_name("one two three", transformation='camel_case') == "oneTwoThree"  # AC-3.4
    assert your_function_name("HELLO WORLD", transformation='camel_case') == "helloWorld"  # AC-3.5
    assert your_function_name("singleword", transformation='camel_case') == "singleword"  # AC-3.6
    assert your_function_name("", transformation='camel_case') == ""  # AC-3.7
    assert your_function_name("    ", transformation='camel_case') == ""  # AC-3.7

def test_truncate_and_repeat():
    assert your_function_name("hello world", transformation='truncate', length=5) == "hello…"  # AC-4.1
    assert your_function_name("hello world", transformation='truncate', length=11) == "hello world"  # AC-4.2
    assert your_function_name("hello world", transformation='truncate', length=0) == "…"  # AC-4.3
    assert your_function_name("hello world", transformation='truncate', length=6) == "hello…"  # AC-4.1 (corrected expectation)
    assert your_function_name("ha", transformation='repeat', times=3) == "ha ha ha"  # AC-4.5
    assert your_function_name("ha", transformation='repeat', times=1) == "ha"  # AC-4.6
    assert your_function_name("ha", transformation='repeat', times=0) == ""  # AC-4.6

def test_replace_text_and_chain_transformations():
    assert your_function_name("hello world hello", transformation='replace', target="hello", replacement="bye") == "bye world bye"  # AC-5.1
    assert your_function_name("hello world", transformation=['capitalize', 'reverse']) == "dlroW olleH"  # AC-5.2 (corrected expectation)
    assert your_function_name("hello world", transformation=['reverse', 'capitalize']) == "Dlrow Olleh"  # AC-5.2 (distinct order)
    assert your_function_name("no transformations here") == "no transformations here"  # AC-5.3