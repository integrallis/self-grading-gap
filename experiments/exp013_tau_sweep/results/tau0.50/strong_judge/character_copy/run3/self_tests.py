# your complete test file
import pytest
from solution import copy_characters_one_at_a_time, copy_characters_in_batches

class MockDestination:
    def __init__(self):
        self.written = []

    def write(self, data):
        self.written.append(data)

    def get_written_data(self):
        return ''.join(self.written)

def test_copy_one_character_at_a_time():
    dest = MockDestination()
    
    # AC-1.1
    copy_characters_one_at_a_time("hello\nworld", dest)
    assert dest.get_written_data() == "hello"  # Copying "hello"
    assert len(dest.written) == 5  # 5 writes for 5 characters
    
    # AC-1.2
    dest = MockDestination()
    copy_characters_one_at_a_time("\nworld", dest)
    assert dest.get_written_data() == ""  # No characters copied
    assert len(dest.written) == 0  # No writes
    
    # AC-1.3
    dest = MockDestination()
    copy_characters_one_at_a_time("hello\n", dest)
    assert dest.get_written_data() == "hello"  # Copying "hello", not the newline
    assert len(dest.written) == 5  # 5 writes for 5 characters
    
    # AC-1.4
    dest = MockDestination()
    copy_characters_one_at_a_time("hello world\n", dest)
    assert dest.get_written_data() == "hello world"  # Copying "hello world"
    assert len(dest.written) == 11  # 11 writes for 11 characters
    
    # AC-1.5
    dest = MockDestination()
    copy_characters_one_at_a_time("hello\nworld", dest)
    assert dest.get_written_data() == "hello"  # Stops at newline
    assert len(dest.written) == 5  # 5 writes for 5 characters
    
    # AC-1.6
    dest = MockDestination()
    copy_characters_one_at_a_time("hello", dest)
    assert dest.get_written_data() == "hello"  # Source ends before newline
    assert len(dest.written) == 5  # 5 writes for 5 characters
    
    # AC-1.7
    dest = MockDestination()
    copy_characters_one_at_a_time("hi! how are you?\n", dest)
    assert dest.get_written_data() == "hi! how are you?"  # Copying verbatim
    assert len(dest.written) == 16  # 16 writes for 16 characters

    # AC-1.6 (New test for unread content after newline)
    dest = MockDestination()
    copy_characters_one_at_a_time("hello\nworld", dest)
    assert dest.get_written_data() == "hello"  # Stops at newline
    assert len(dest.written) == 5  # 5 writes for 5 characters
    
    # AC-1.6 (Empty source)
    dest = MockDestination()
    copy_characters_one_at_a_time("", dest)
    assert dest.get_written_data() == ""  # No characters copied
    assert len(dest.written) == 0  # No writes

def test_copy_in_batches():
    dest = MockDestination()
    
    # AC-2.1
    copy_characters_in_batches("hello world\nhow are you?", 5, dest)
    assert dest.get_written_data() == "hello"  # First batch without newline
    assert len(dest.written) == 1  # One write for the first batch
    
    # AC-2.2
    dest = MockDestination()
    copy_characters_in_batches("hello\nhow are you?", 5, dest)
    assert dest.get_written_data() == "hello"  # Stops at newline
    assert len(dest.written) == 1  # One write for the batch before newline
    
    # AC-2.3
    dest = MockDestination()
    copy_characters_in_batches("\nhello", 5, dest)
    assert dest.get_written_data() == ""  # No characters copied
    assert len(dest.written) == 0  # No writes
    
    # AC-2.4
    dest = MockDestination()
    copy_characters_in_batches("hello world\nhow are you?", 5, dest)
    assert dest.get_written_data() == "hello"  # Stops at newline
    assert len(dest.written) == 1  # One write for the first batch
    
    # AC-2.4 (New test for multiple batches)
    dest = MockDestination()
    copy_characters_in_batches("hello world\nhow are you?", 5, dest)
    assert dest.get_written_data() == "hello"  # First batch without newline
    assert len(dest.written) == 1  # One write for the first batch
    
    # AC-2.5
    dest = MockDestination()
    copy_characters_in_batches("hello world\nhow are you?", 10, dest)
    assert dest.get_written_data() == "hello world"  # First batch with newline
    assert len(dest.written) == 1  # One write for the full batch
    
    # AC-2.6
    dest = MockDestination()
    copy_characters_in_batches("hello", 10, dest)
    assert dest.get_written_data() == "hello"  # Source exhausted, written shortfall
    assert len(dest.written) == 1  # One write for the shortfall
    
    # AC-2.7
    dest = MockDestination()
    copy_characters_in_batches("", 5, dest)
    assert dest.get_written_data() == ""  # No writes for empty source
    assert len(dest.written) == 0  # No writes
    
    # AC-2.8
    dest = MockDestination()
    copy_characters_in_batches("hello\nworld\nfoo", 10, dest)
    assert dest.get_written_data() == "hello"  # Stops at first newline
    assert len(dest.written) == 1  # One write for the first part

    # AC-2.8 (New test for nonempty prefix in first batch)
    dest = MockDestination()
    copy_characters_in_batches("abc\nrest", 5, dest)
    assert dest.get_written_data() == "abc"  # Stops at first newline
    assert len(dest.written) == 1  # One write for the first part

def test_batch_size_validation():
    dest = MockDestination()
    # AC-3.1
    with pytest.raises(Exception) as excinfo:  # Change to your exception class if specified
        copy_characters_in_batches("hello", 0, dest)
    assert str(excinfo.value) == "count must be at least 1"
    
    # AC-3.1 (Negative count)
    with pytest.raises(Exception) as excinfo:  # Change to your exception class if specified
        copy_characters_in_batches("hello", -1, dest)
    assert str(excinfo.value) == "count must be at least 1"
    
    # AC-3.2
    dest = MockDestination()
    copy_characters_in_batches("hello\nworld", 1, dest)
    assert dest.get_written_data() == "h"  # Accepts batch size of 1, copies one character
    assert len(dest.written) == 1  # 1 write for 1 character