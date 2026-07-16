from solution import copy_characters
import pytest

class TestDouble:
    def __init__(self):
        self.written = []
    
    def write(self, data):
        self.written.append(data)
    
    def get_written(self):
        return ''.join(self.written)

def test_copy_one_character_at_a_time():
    dest = TestDouble()
    
    # AC-1.1: Characters before the newline are written one by one, in source order.
    copy_characters("hello\nworld", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]
    
    # AC-1.2: When the very first character is a newline, nothing is written.
    dest = TestDouble()
    copy_characters("\nworld", dest.write)
    assert dest.written == []  # expected: []
    
    # AC-1.3: The terminating newline itself is never written.
    dest = TestDouble()
    copy_characters("hello\n", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]
    
    # AC-1.4: Content after the newline is never copied.
    dest = TestDouble()
    copy_characters("hello\nworld", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]
    
    # AC-1.5: Reading stops immediately after the newline is consumed.
    dest = TestDouble()
    copy_characters("hello\nworld", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]
    
    # AC-1.6: A source that runs out before any newline ends the copy.
    dest = TestDouble()
    copy_characters("hello", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]
    
    # AC-1.7: Ordinary characters — including spaces and punctuation — are copied verbatim.
    dest = TestDouble()
    copy_characters("hello, world!\nfoo", dest.write)
    assert dest.written == ["h", "e", "l", "l", "o", ",", " ", "w", "o", "r", "l", "d", "!"]  # expected: ["h", "e", "l", "l", "o", ",", " ", "w", "o", "r", "l", "d", "!"]

def test_copy_in_batches():
    dest = TestDouble()
    
    # AC-2.1: A batch containing no newline is written whole, as a single write.
    copy_characters("hello world", dest.write, batch_size=11)
    assert dest.written == ["hello world"]  # expected: ["hello world"]
    
    # AC-2.2: A batch containing the newline is written only up to, and excluding, the newline.
    dest = TestDouble()
    copy_characters("hello\nworld", dest.write, batch_size=11)
    assert dest.written == ["hello"]  # expected: ["hello"]
    
    # AC-2.3: A source that begins with a newline produces no writes.
    dest = TestDouble()
    copy_characters("\nworld", dest.write, batch_size=11)
    assert dest.written == []  # expected: []
    
    # AC-2.4: Batches keep being read and written until the newline appears.
    dest = TestDouble()
    copy_characters("hello world\nfoo bar", dest.write, batch_size=5)
    assert dest.written == ["hello", " world"]  # expected: ["hello", " world"]
    
    # AC-2.5: Nothing beyond the first newline is ever written.
    dest = TestDouble()
    copy_characters("hello\nworld", dest.write, batch_size=5)
    assert dest.written == ["hello"]  # expected: ["hello"]
    
    # AC-2.6: A batch shorter than requested means the source is exhausted.
    dest = TestDouble()
    copy_characters("hello", dest.write, batch_size=10)
    assert dest.written == ["hello"]  # expected: ["hello"]
    
    # AC-2.7: An empty source produces no writes at all.
    dest = TestDouble()
    copy_characters("", dest.write, batch_size=5)
    assert dest.written == []  # expected: []
    
    # AC-2.8: When a batch holds more than one newline, copying is cut at the first.
    dest = TestDouble()
    copy_characters("hello\nworld\nfoo", dest.write, batch_size=10)
    assert dest.written == ["hello"]  # expected: ["hello"]

def test_batch_size_validation():
    dest = TestDouble()
    
    # AC-3.1: A batch size below 1 is rejected with an error.
    with pytest.raises(Exception, match=r"^count must be at least 1$"):
        copy_characters("hello", dest.write, batch_size=0)
    
    # Test negative batch size
    with pytest.raises(Exception, match=r"^count must be at least 1$"):
        copy_characters("hello", dest.write, batch_size=-1)
    
    # AC-3.2: A batch size of exactly 1 is accepted and copies one character per write.
    dest = TestDouble()
    copy_characters("hello\nworld", dest.write, batch_size=1)
    assert dest.written == ["h", "e", "l", "l", "o"]  # expected: ["h", "e", "l", "l", "o"]