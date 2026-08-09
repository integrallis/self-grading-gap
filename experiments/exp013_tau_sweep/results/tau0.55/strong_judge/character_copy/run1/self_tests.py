from solution import copy_one_by_one, copy_in_batches

def test_copy_one_character_at_a_time():
    # AC-1.1: Characters before the newline are written one by one, in source order.
    dest = []
    copy_one_by_one("Hello\nWorld", dest)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # "Hello" before newline

    # AC-1.2: When the very first character is a newline, nothing is written.
    dest = []
    copy_one_by_one("\nHello", dest)
    assert dest == []  # No characters written

    # AC-1.3: The terminating newline itself is never written.
    dest = []
    copy_one_by_one("Hello\nWorld", dest)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # Newline not included

    # AC-1.4: Content after the newline is never copied.
    dest = []
    copy_one_by_one("Hello\nWorld", dest)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # "World" not included

    # AC-1.5: Reading stops immediately after the newline is consumed; later source content is left unread.
    class InstrumentedSource:
        def __init__(self, source):
            self.source = source
            self.index = 0
        
        def read(self, n):
            if self.index < len(self.source):
                result = self.source[self.index:self.index+n]
                self.index += len(result)
                return result
            return ''
        
        def unread(self):
            return self.source[self.index:]

    source = InstrumentedSource("Hello\nWorld")
    dest = []
    copy_one_by_one(source, dest)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # "World" not read
    assert source.unread() == "World"  # Confirm "World" is still unread

    # AC-1.6: A source that runs out before any newline ends the copy, with everything read so far already written.
    dest = []
    copy_one_by_one("Hello", dest)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # Entire string copied

    # AC-1.7: Ordinary characters — including spaces and punctuation — are copied verbatim.
    dest = []
    copy_one_by_one("Hello, World!\nGoodbye", dest)
    assert dest == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!']  # All ordinary characters copied


def test_copy_in_batches():
    # AC-2.1: A batch containing no newline is written whole, as a single write.
    dest = []
    copy_in_batches("HelloWorld", dest, batch_size=10)
    assert dest == ['HelloWorld']  # Whole batch copied

    # AC-2.2: A batch containing the newline is written only up to, and excluding, the newline.
    dest = []
    copy_in_batches("Hello\nWorld", dest, batch_size=10)
    assert dest == ['Hello']  # Only "Hello" before newline copied

    # AC-2.3: A source that begins with a newline produces no writes.
    dest = []
    copy_in_batches("\nHello", dest, batch_size=10)
    assert dest == []  # No characters written

    # AC-2.4: Batches keep being read and written until the newline appears, each full batch delivered as one write.
    dest = []
    copy_in_batches("HelloWorld\nGoodbye", dest, batch_size=5)
    assert dest == ['Hello', 'World']  # Both batches before newline copied

    # AC-2.5: Nothing beyond the first newline is ever written, even when the newline falls in the middle of a batch.
    dest = []
    copy_in_batches("HelloWorld\nGoodbye", dest, batch_size=7)
    assert dest == ['HelloWo', 'rld']  # Cut at first newline and write prefix

    # AC-2.6: A batch shorter than requested means the source is exhausted: the shortfall is still written, then copying stops.
    dest = []
    copy_in_batches("Hello", dest, batch_size=10)
    assert dest == ['Hello']  # Whole string copied as one batch

    # AC-2.7: An empty source produces no writes at all.
    dest = []
    copy_in_batches("", dest, batch_size=10)
    assert dest == []  # No writes from empty source

    # AC-2.8: When a batch holds more than one newline, copying is cut at the first, not the last.
    dest = []
    copy_in_batches("Hello\nWorld\nGoodbye", dest, batch_size=10)
    assert dest == ['Hello']  # Cut at first newline


def test_batch_size_validation():
    # AC-3.1: A batch size below 1 is rejected with an error whose message is exactly "count must be at least 1".
    import pytest
    with pytest.raises(Exception) as excinfo:
        copy_in_batches("Hello", [], batch_size=0)
    assert str(excinfo.value) == "count must be at least 1"  # Exact error message

    # Additional test for batch size below 1
    with pytest.raises(Exception) as excinfo:
        copy_in_batches("Hello", [], batch_size=-1)
    assert str(excinfo.value) == "count must be at least 1"  # Exact error message

    # AC-3.2: A batch size of exactly 1 is accepted and copies one character per write.
    dest = []
    copy_in_batches("Hello\nWorld", dest, batch_size=1)
    assert dest == ['H', 'e', 'l', 'l', 'o']  # Each character copied one by one