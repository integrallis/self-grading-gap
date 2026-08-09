import pytest
from solution import copy_characters_one_at_a_time, copy_characters_in_batches

class WriteSpy:
    def __init__(self):
        self.written = []
    
    def write(self, content):
        if content:  # Ensure we only append non-empty content
            self.written.append(content)
    
    def get_written(self):
        return ''.join(self.written)

class SourceSpy:
    def __init__(self, content):
        self.content = content
        self.index = 0
    
    def read(self, count):
        if self.index >= len(self.content):
            return ''
        read_content = self.content[self.index:self.index + count]
        self.index += len(read_content)
        return read_content
    
    def reset(self):
        self.index = 0

def test_copy_characters_one_at_a_time():
    # Test copying characters before the first newline
    source = SourceSpy("Hello\nWorld")
    destination = WriteSpy()
    copy_characters_one_at_a_time(source, destination)
    assert destination.get_written() == "Hello"  # AC-1.1, AC-1.3, AC-1.4

    # Test with first character as newline
    source.reset()
    source.content = "\nWorld"
    destination = WriteSpy()
    copy_characters_one_at_a_time(source, destination)
    assert destination.get_written() == ""  # AC-1.2

    # Test with newline consumed
    source.reset()
    source.content = "Hello\nWorld"
    destination = WriteSpy()
    copy_characters_one_at_a_time(source, destination)
    assert destination.get_written() == "Hello"  # AC-1.5, AC-1.6

    # Test with spaces and punctuation
    source.reset()
    source.content = "Hello, World!\nNext Line"
    destination = WriteSpy()
    copy_characters_one_at_a_time(source, destination)
    assert destination.get_written() == "Hello, World!"  # AC-1.7

    # Test EOF without newline
    source.reset()
    source.content = "Hello World"
    destination = WriteSpy()
    copy_characters_one_at_a_time(source, destination)
    assert destination.get_written() == "Hello World"  # AC-1.6

def test_copy_characters_in_batches():
    # Test full batch with no newline
    source = SourceSpy("Hello World")
    destination = WriteSpy()
    copy_characters_in_batches(source, 5, destination)
    assert destination.get_written() == "Hello"  # AC-2.1

    # Test batch containing a newline
    source.reset()
    source.content = "Hello\nWorld"
    destination = WriteSpy()
    copy_characters_in_batches(source, 10, destination)
    assert destination.get_written() == "Hello"  # AC-2.2

    # Test source that begins with a newline
    source.reset()
    source.content = "\nWorld"
    destination = WriteSpy()
    copy_characters_in_batches(source, 5, destination)
    assert destination.get_written() == ""  # AC-2.3

    # Test batching until newline
    source.reset()
    source.content = "Hello\nWorld!"
    destination = WriteSpy()
    copy_characters_in_batches(source, 3, destination)
    assert destination.get_written() == "Hel"  # AC-2.4
    
    # Test content after the first newline
    source.reset()
    source.content = "Hello\nWorld!\nAgain"
    destination = WriteSpy()
    copy_characters_in_batches(source, 5, destination)
    assert destination.get_written() == "Hello"  # AC-2.5

    # Test short final batch
    source.reset()
    source.content = "Hello"
    destination = WriteSpy()
    copy_characters_in_batches(source, 10, destination)
    assert destination.get_written() == "Hello"  # AC-2.6

    # Test empty source
    source = SourceSpy("")
    destination = WriteSpy()
    copy_characters_in_batches(source, 5, destination)
    assert destination.get_written() == ""  # AC-2.7

    # Test multiple newlines
    source.reset()
    source.content = "Hello\nWorld\nAgain"
    destination = WriteSpy()
    copy_characters_in_batches(source, 10, destination)
    assert destination.get_written() == "Hello"  # AC-2.8

def test_batch_size_validation():
    with pytest.raises(Exception, match="count must be at least 1"):
        copy_characters_in_batches("Hello World", 0, WriteSpy())
    with pytest.raises(Exception, match="count must be at least 1"):
        copy_characters_in_batches("Hello World", -1, WriteSpy())
    
    destination = WriteSpy()
    source = SourceSpy("Hello")
    copy_characters_in_batches(source, 1, destination)
    assert destination.get_written() == "Hello"  # AC-3.2