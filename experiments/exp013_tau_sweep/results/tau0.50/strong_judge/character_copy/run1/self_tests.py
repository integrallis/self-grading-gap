import pytest
from solution import copy_characters_one_at_a_time, copy_characters_in_batches

def test_copy_one_character_at_a_time():
    # AC-1.1: Characters before the newline are written one by one, in source order.
    destination = []
    copy_characters_one_at_a_time("Hello\nWorld", destination.append)
    assert destination == list("Hello")  # Each character written one by one to destination
    # AC-1.2: When the very first character is a newline, nothing is written.
    destination = []
    copy_characters_one_at_a_time("\nWorld", destination.append)
    assert destination == []  # No writes
    # AC-1.3: The terminating newline itself is never written.
    destination = []
    copy_characters_one_at_a_time("Hello\n", destination.append)
    assert destination == list("Hello")  # Newline is not written
    # AC-1.4: Content after the newline is never copied.
    destination = []
    copy_characters_one_at_a_time("Hello\nWorld", destination.append)
    assert destination == list("Hello")  # "World" is ignored
    # AC-1.5: Reading stops immediately after the newline is consumed.
    class InstrumentedSource:
        def __init__(self, data):
            self.data = data
            self.read_count = 0
        
        def read(self, n):
            if self.read_count >= len(self.data):
                return ''
            result = self.data[self.read_count:self.read_count + n]
            self.read_count += len(result)
            if '\n' in result:
                result = result[:result.index('\n')]
            return result
            
    destination = []
    source = InstrumentedSource("Hello\nWorld\n!")
    copy_characters_one_at_a_time(source.read, destination.append)
    assert destination == list("Hello")  # Stops after first newline
    assert source.read_count == len("Hello")  # Ensure it read only up to the newline
    # AC-1.6: A source that runs out before any newline ends the copy.
    destination = []
    copy_characters_one_at_a_time("Hel", destination.append)
    assert destination == list("Hel")  # All characters are copied
    # AC-1.7: Ordinary characters are copied verbatim.
    destination = []
    copy_characters_one_at_a_time("Hello, World!", destination.append)
    assert destination == list("Hello, World!")  # All copied as is

def test_copy_in_batches():
    # AC-2.1: A batch containing no newline is written whole.
    destination = []
    copy_characters_in_batches("Hello World", 5, destination.append)
    assert destination == ["Hello World"]  # Full batch, no newline written
    # AC-2.2: A batch containing the newline is written only up to, excluding, the newline.
    destination = []
    copy_characters_in_batches("Hello\nWorld", 5, destination.append)
    assert destination == ["Hello"]  # Only "Hello" before newline
    # AC-2.3: A source that begins with a newline produces no writes.
    destination = []
    copy_characters_in_batches("\nWorld", 5, destination.append)
    assert destination == []  # First char is newline, nothing copied
    # AC-2.4: Batches keep being read and written until the newline appears.
    destination = []
    copy_characters_in_batches("Hello World\nThis is a test", 5, destination.append)
    assert destination == ["Hello World"]  # Stops at newline
    # AC-2.5: Nothing beyond the first newline is ever written.
    destination = []
    copy_characters_in_batches("Hello\nWorld", 10, destination.append)
    assert destination == ["Hello"]  # Stops at newline
    # AC-2.6: A batch shorter than requested means the source is exhausted.
    destination = []
    copy_characters_in_batches("Hello", 10, destination.append)
    assert destination == ["Hello"]  # Full copy, source exhausted
    # AC-2.7: An empty source produces no writes at all.
    destination = []
    copy_characters_in_batches("", 5, destination.append)
    assert destination == []  # Empty source, nothing copied
    # AC-2.8: When a batch holds more than one newline, copying is cut at the first.
    destination = []
    copy_characters_in_batches("Hello\nthere\nfriend", 10, destination.append)
    assert destination == ["Hello"]  # Stops at first newline

def test_batch_size_validation():
    # AC-3.1: A batch size below 1 is rejected with the specified error message.
    with pytest.raises(Exception) as exc_info:
        copy_characters_in_batches("Hello World", 0, lambda x: None)
    assert str(exc_info.value) == "count must be at least 1"  # Check exact error message
    # Add a check for negative batch size
    with pytest.raises(Exception) as exc_info:
        copy_characters_in_batches("Hello World", -1, lambda x: None)
    assert str(exc_info.value) == "count must be at least 1"  # Check exact error message
    # AC-3.2: A batch size of exactly 1 is accepted.
    destination = []
    copy_characters_in_batches("Hello", 1, destination.append)
    assert destination == ["H", "e", "l", "l", "o"]  # One character per write