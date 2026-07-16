import pytest
from solution import copy_one_at_a_time, copy_in_batches

# Test for copying one character at a time
def test_copy_one_at_a_time_characters_before_newline():
    destination = []
    source = "Hello\nWorld"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'e', 'l', 'l', 'o']
    assert destination == ['H', 'e', 'l', 'l', 'o']

def test_copy_one_at_a_time_first_character_is_newline():
    destination = []
    source = "\nHello"
    copy_one_at_a_time(source, destination)
    # Expecting: []
    assert destination == []

def test_copy_one_at_a_time_terminating_newline_never_written():
    destination = []
    source = "Hello\nWorld"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'e', 'l', 'l', 'o']
    assert destination == ['H', 'e', 'l', 'l', 'o']

def test_copy_one_at_a_time_content_after_newline_never_copied():
    destination = []
    source = "Hello\nWorld"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'e', 'l', 'l', 'o']
    assert destination == ['H', 'e', 'l', 'l', 'o']

def test_copy_one_at_a_time_reading_stops_after_newline():
    destination = []
    source = "Hello\nWorld"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'e', 'l', 'l', 'o']
    assert destination == ['H', 'e', 'l', 'l', 'o']

def test_copy_one_at_a_time_source_runs_dry_before_newline():
    destination = []
    source = "Hi"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'i']
    assert destination == ['H', 'i']

def test_copy_one_at_a_time_ordinary_characters_copied_verbatim():
    destination = []
    source = "Hello, World!"
    copy_one_at_a_time(source, destination)
    # Expecting: ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!']
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!']

# Test for copying in batches
def test_copy_in_batches_no_newline_in_batch():
    destination = []
    source = "Hello, World!"
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: ['Hello', ', Wor', 'ld!']
    assert destination == ['Hello', ', Wor', 'ld!']

def test_copy_in_batches_batch_contains_newline():
    destination = []
    source = "Hello\nWorld"
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: ['Hello']
    assert destination == ['Hello']

def test_copy_in_batches_source_starts_with_newline():
    destination = []
    source = "\nHello"
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: []
    assert destination == []

def test_copy_in_batches_batches_until_newline():
    destination = []
    source = "Hello\nWorld\nAgain"
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: ['Hello']
    assert destination == ['Hello']

def test_copy_in_batches_nothing_beyond_first_newline_written():
    destination = []
    source = "Hello\nWorld"
    copy_in_batches(source, destination, batch_size=10)
    # Expecting: ['Hello']
    assert destination == ['Hello']

def test_copy_in_batches_batch_shorter_than_requested():
    destination = []
    source = "Hi"
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: ['Hi']
    assert destination == ['Hi']

def test_copy_in_batches_empty_source():
    destination = []
    source = ""
    copy_in_batches(source, destination, batch_size=5)
    # Expecting: []
    assert destination == []

def test_copy_in_batches_when_batch_holds_more_than_one_newline():
    destination = []
    source = "Hello\nWorld\nAgain"
    copy_in_batches(source, destination, batch_size=20)
    # Expecting: ['Hello']
    assert destination == ['Hello']

# Test for batch size validation
def test_batch_size_validation_below_one():
    with pytest.raises(Exception) as excinfo:
        copy_in_batches("Hello", [], batch_size=0)
    assert str(excinfo.value) == "count must be at least 1"

def test_batch_size_validation_negative_size():
    with pytest.raises(Exception) as excinfo:
        copy_in_batches("Hello", [], batch_size=-1)
    assert str(excinfo.value) == "count must be at least 1"

def test_batch_size_validation_exactly_one():
    destination = []
    source = "Hello"
    copy_in_batches(source, destination, batch_size=1)
    # Expecting: ['H', 'e', 'l', 'l', 'o']
    assert destination == ['H', 'e', 'l', 'l', 'o']