import pytest
from solution import copy_one_at_a_time, copy_in_batches, validate_batch_size

class MockDestination:
    def __init__(self):
        self.content = ""
    
    def write(self, text):
        self.content += text

def test_copy_one_at_a_time_with_characters_before_newline():
    source = "Hello, World!\nThis is a test."
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "Hello, World!" (everything before the newline)
    assert destination.content == "Hello, World!"

def test_copy_one_at_a_time_with_newline_first():
    source = "\nThis should not be copied."
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "" (nothing should be written)
    assert destination.content == ""

def test_copy_one_at_a_time_with_only_newline():
    source = "\n"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "" (nothing should be written)
    assert destination.content == ""

def test_copy_one_at_a_time_with_no_newline():
    source = "This is a line without a newline"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "This is a line without a newline" (everything copied since no newline)
    assert destination.content == "This is a line without a newline"

def test_copy_one_at_a_time_with_newline_in_middle():
    source = "Line 1\nLine 2"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "Line 1" (only up to the first newline)
    assert destination.content == "Line 1"

def test_copy_one_at_a_time_with_trailing_content():
    source = "Hello\nWorld!"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "Hello" (nothing after the newline)
    assert destination.content == "Hello"

def test_copy_one_at_a_time_with_exhausted_source_before_newline():
    source = "Hi"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "Hi" (entire content copied as no newline is present)
    assert destination.content == "Hi"

def test_copy_one_at_a_time_with_spaces_and_punctuation():
    source = "Hello, World!\nNext line."
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "Hello, World!" (spaces and punctuation copied)
    assert destination.content == "Hello, World!"

def test_copy_one_at_a_time_writes_one_character_per_write():
    source = "ABC\nNext"
    destination = MockDestination()
    copy_one_at_a_time(source, destination.write)
    # Expected: "ABC" (each character is written one at a time)
    assert destination.content == "ABC"

def test_copy_one_at_a_time_stops_reading_after_newline():
    class FailingSource:
        def __init__(self, content):
            self.content = content
            self.index = 0
        
        def read(self, n):
            if self.index < len(self.content):
                result = self.content[self.index:self.index + n]
                self.index += len(result)
                return result
            return ""
        
    source = FailingSource("Line 1\nLine 2")
    destination = MockDestination()
    copy_one_at_a_time(source.read, destination.write)
    # Ensure that reading after newline fails
    assert source.index == 6  # Should stop at the newline

def test_copy_in_batches_with_no_newline():
    source = "Hello, World!"
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hello, World!" (copying continues until exhaustion)
    assert destination.content == "Hello, World!"

def test_copy_in_batches_with_newline():
    source = "Hello, World!\nNext line."
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hello, World!" (first newline occurs after full prefix)
    assert destination.content == "Hello, World!"

def test_copy_in_batches_with_newline_first():
    source = "\nThis should not be copied."
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "" (nothing should be written)
    assert destination.content == ""

def test_copy_in_batches_with_exhausted_source():
    source = "Hi"
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hi" (entire content copied as source is exhausted)
    assert destination.content == "Hi"

def test_copy_in_batches_with_multiple_newlines():
    source = "Hello\nWorld\n!"
    destination = MockDestination()
    batch_size = 10
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hello" (only up to the first newline)
    assert destination.content == "Hello"

def test_copy_in_batches_writes_full_batches():
    source = "Hello, World!\nThis is a test."
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hello, World!" (each full batch written before the newline)
    assert destination.content == "Hello, World!"

def test_copy_in_batches_with_empty_source():
    source = ""
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "" (no writes occur with empty source)
    assert destination.content == ""

def test_copy_in_batches_short_final_batch():
    source = "Hi"
    destination = MockDestination()
    batch_size = 5
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "Hi" (the shortfall is written once before copying stops)
    assert destination.content == "Hi"

def test_validate_batch_size_with_valid_size():
    batch_size = 1
    # Expected: No exception is raised
    validate_batch_size(batch_size)

def test_validate_batch_size_with_invalid_size_below_one():
    batch_size = 0
    # Expected: An error with message "count must be at least 1"
    with pytest.raises(Exception) as e:
        validate_batch_size(batch_size)
    assert str(e.value) == "count must be at least 1"

def test_validate_batch_size_with_invalid_size_negative():
    batch_size = -1
    # Expected: An error with message "count must be at least 1"
    with pytest.raises(Exception) as e:
        validate_batch_size(batch_size)
    assert str(e.value) == "count must be at least 1"

def test_copy_in_batches_with_batch_size_one():
    source = "ABC\nNext"
    destination = MockDestination()
    batch_size = 1
    copy_in_batches(source, destination.write, batch_size)
    # Expected: "ABC" (each character is delivered in a separate write)
    assert destination.content == "ABC"