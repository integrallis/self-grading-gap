import pytest
from solution import copy_one_character, copy_in_batches

# Test for US-1: Copy one character at a time

def test_copy_one_character():
    source = "Hello\nWorld"
    destination = []
    copy_one_character(source, destination)
    assert destination == ['H', 'e', 'l', 'l', 'o']  # First line before newline

def test_copy_one_character_first_newline():
    source = "\nHello"
    destination = []
    copy_one_character(source, destination)
    assert destination == []  # First character is newline, nothing written

def test_copy_one_character_terminating_newline():
    source = "Hello\nWorld"
    destination = []
    copy_one_character(source, destination)
    assert destination[-1] != '\n'  # Last character should not be newline

def test_copy_one_character_after_newline():
    source = "Hello\nWorld"
    destination = []
    copy_one_character(source, destination)
    # After newline, only 'Hello' should be copied
    assert ''.join(destination) == 'Hello'

def test_copy_one_character_source_exhausted():
    source = "Hello"
    destination = []
    copy_one_character(source, destination)
    assert ''.join(destination) == 'Hello'  # Source runs dry, all written

def test_copy_one_character_ordinary_characters():
    source = "Hello, World!"
    destination = []
    copy_one_character(source, destination)
    assert ''.join(destination) == 'Hello, World!'  # All characters copied verbatim

def test_copy_one_character_stops_reading_after_newline():
    source = "Hello\nWorld"
    destination = []
    copy_one_character(source, destination)
    # Ensure that "World" is not read after the newline
    assert ''.join(destination) == 'Hello'

# Test for US-2: Copy in batches

def test_copy_in_batches_no_newline():
    source = "Hello, World!"
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == ['Hello', ', Wor', 'ld!']  # Full batches and final short batch written

def test_copy_in_batches_with_newline():
    source = "Hello\nWorld"
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == ['Hello']  # Batch written up to newline, only "Hello" should be written

def test_copy_in_batches_starts_with_newline():
    source = "\nHello"
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == []  # Starts with newline, no writes

def test_copy_in_batches_multiple_batches():
    source = "Hello, World!\nGoodbye!"
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == ['Hello', ', Wor', 'ld!']  # Only first line copied

def test_copy_in_batches_exhausted_source():
    source = "Hi"
    destination = []
    copy_in_batches(source, destination, batch_size=10)
    assert destination == ['Hi']  # Short batch as source exhausted

def test_copy_in_batches_empty_source():
    source = ""
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == []  # Empty source produces no writes

def test_copy_in_batches_multiple_newlines():
    source = "a\nb\nc"
    destination = []
    copy_in_batches(source, destination, batch_size=5)
    assert destination == ['a']  # Only first line copied

# Test for US-3: Batch size validation

def test_batch_size_validation_below_one():
    with pytest.raises(Exception) as exc_info:
        copy_in_batches("Hello", [], batch_size=0)  # Batch size below 1
    assert str(exc_info.value) == "count must be at least 1"  # Exact message

    with pytest.raises(Exception) as exc_info:
        copy_in_batches("Hello", [], batch_size=-1)  # Negative batch size
    assert str(exc_info.value) == "count must be at least 1"  # Exact message

def test_batch_size_validation_exactly_one():
    source = "Hello"
    destination = []
    copy_in_batches(source, destination, batch_size=1)
    assert destination == ['H', 'e', 'l', 'l', 'o']  # One character per write