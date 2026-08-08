from solution import copy_characters, copy_in_batches, validate_batch_size

class WriteRecorder:
    def __init__(self):
        self.writes = []
    
    def write(self, content):
        self.writes.append(content)

def test_copy_characters_one_by_one():
    # Test that characters before the newline are written one by one.
    destination = WriteRecorder()
    copy_characters("hello\nworld", destination)
    assert destination.writes == ["hello"]  # Only the first line is copied
    destination = WriteRecorder()
    copy_characters("\nworld", destination)
    assert destination.writes == []  # First character is newline, nothing written
    destination = WriteRecorder()
    copy_characters("hello", destination)
    assert destination.writes == ["hello"]  # No newline, all characters written

def test_copy_characters_newline_handling():
    # Test that the terminating newline itself is never written.
    destination = WriteRecorder()
    copy_characters("hello\nworld", destination)
    assert destination.writes == ["hello"]  # Newline not included
    destination = WriteRecorder()
    copy_characters("hello\n", destination)
    assert destination.writes == ["hello"]  # Newline at the end, still not included
    destination = WriteRecorder()
    copy_characters("\n", destination)
    assert destination.writes == []  # Only newline, nothing written

def test_copy_characters_content_after_newline_not_written():
    # Test that content after the newline is never copied.
    destination = WriteRecorder()
    copy_characters("hello\nworld", destination)
    assert destination.writes == ["hello"]  # "world" is after newline, not copied
    destination = WriteRecorder()
    copy_characters("line1\nline2\nline3", destination)
    assert destination.writes == ["line1"]  # Stops at first newline

def test_copy_characters_exhausted_source():
    # Test that a source that runs dry before any newline ends the copy.
    destination = WriteRecorder()
    copy_characters("hello", destination)
    assert destination.writes == ["hello"]  # Source unchanged, no newline present
    destination = WriteRecorder()
    copy_characters("", destination)
    assert destination.writes == []  # Empty source, no writes at all

def test_copy_characters_ordianry_characters():
    # Test that ordinary characters are copied verbatim.
    destination = WriteRecorder()
    copy_characters("abc def! 123", destination)
    assert destination.writes == ["abc def! 123"]  # Spaces and punctuation included

def test_copy_in_batches():
    # Test copying in fixed-size batches.
    destination = WriteRecorder()
    copy_in_batches("hello\nworld", 5, destination)
    assert destination.writes == ["hello"]  # Batch of 5 includes no newline
    destination = WriteRecorder()
    copy_in_batches("hello world\nfoo", 8, destination)
    assert destination.writes == ["hello wo", "rld"]  # Stops at newline
    destination = WriteRecorder()
    copy_in_batches("\nhello", 3, destination)
    assert destination.writes == []  # Source starts with newline, nothing written
    destination = WriteRecorder()
    copy_in_batches("hello world", 15, destination)
    assert destination.writes == ["hello world"]  # Batch larger than content

def test_copy_in_batches_multiple_batches():
    # Test that batches keep being read and written until the newline appears.
    destination = WriteRecorder()
    copy_in_batches("hello\nworld\nfoo", 5, destination)
    assert destination.writes == ["hello"]  # First batch only
    destination = WriteRecorder()
    copy_in_batches("hello world\nfoo bar\nbaz", 6, destination)
    assert destination.writes == ["hello ", "world"]  # Stops at first newline

def test_copy_in_batches_exhausted_source():
    # Test that a batch shorter than requested means the source is exhausted.
    destination = WriteRecorder()
    copy_in_batches("hi\nthere", 4, destination)
    assert destination.writes == ["hi"]  # Batch size 4, stops at first newline

def test_copy_in_batches_empty_source():
    # Test that an empty source produces no writes at all.
    destination = WriteRecorder()
    copy_in_batches("", 5, destination)
    assert destination.writes == []  # Empty source, no writes

def test_copy_in_batches_newline_in_batch():
    # Test that when a batch holds more than one newline, copying is cut at the first.
    destination = WriteRecorder()
    copy_in_batches("hello\nworld\nfoo", 10, destination)
    assert destination.writes == ["hello"]  # Stops at first newline

def test_validate_batch_size():
    # Test batch size validation.
    validate_batch_size(1)  # Batch size of exactly 1 is accepted
    with pytest.raises(Exception, match=r"^count must be at least 1$"):
        validate_batch_size(0)  # Batch size below 1 should raise an error
    with pytest.raises(Exception, match=r"^count must be at least 1$"):
        validate_batch_size(-5)  # Batch size below 1 should raise an error

def test_copy_characters_stops_after_first_newline():
    destination = WriteRecorder()
    copy_characters("hello\nworld", destination)
    assert destination.writes == ["hello"]  # Stops after first newline

def test_copy_in_batches_no_empty_writes():
    destination = WriteRecorder()
    copy_in_batches("\nhello world", 5, destination)
    assert destination.writes == []  # No writes for initial newline
    destination = WriteRecorder()
    copy_in_batches("", 5, destination)
    assert destination.writes == []  # No writes for empty source

def test_copy_in_batches_short_final_batch():
    destination = WriteRecorder()
    copy_in_batches("hi there\nhow are you?", 10, destination)
    assert destination.writes == ["hi there"]  # Writes short batch then stops