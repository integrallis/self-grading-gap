from solution import copy_characters_one_at_a_time, copy_characters_in_batches, validate_batch_size

def test_copy_one_character_at_a_time():
    # Test AC-1.1: Characters before the newline are written one by one, in source order.
    assert copy_characters_one_at_a_time("Hello\nWorld") == "Hello"  # "Hello" is before newline
    
    # Test AC-1.2: When the very first character is a newline, nothing is written.
    assert copy_characters_one_at_a_time("\nHello") == ""  # First character is newline
    
    # Test AC-1.3: The terminating newline itself is never written.
    assert copy_characters_one_at_a_time("Line1\nLine2") == "Line1"  # Newline not included
    
    # Test AC-1.4: Content after the newline is never copied.
    assert copy_characters_one_at_a_time("First line\nSecond line") == "First line"  # Only first line copied
    
    # Test AC-1.5: Reading stops immediately after the newline is consumed.
    assert copy_characters_one_at_a_time("Stop here\nBut not here") == "Stop here"  # Stops at newline
    
    # Test AC-1.6: A source that runs out before any newline ends the copy.
    assert copy_characters_one_at_a_time("No newline here") == "No newline here"  # Source ends without newline
    
    # Test AC-1.7: Ordinary characters — including spaces and punctuation — are copied verbatim.
    assert copy_characters_one_at_a_time("Hello, world!\nAnother line") == "Hello, world!"  # Punctuation and spaces copied

def test_copy_in_batches():
    # Test AC-2.1: A batch containing no newline is written whole, as a single write.
    assert copy_characters_in_batches("Hello, world!", 5) == "Hello"  # Full batch without newline

    # Test AC-2.2: A batch containing the newline is written only up to, and excluding, the newline.
    assert copy_characters_in_batches("Hello\nWorld", 5) == "Hello"  # Stops at newline
    
    # Test AC-2.3: A source that begins with a newline produces no writes.
    assert copy_characters_in_batches("\nHello", 5) == ""  # First character is newline
    
    # Test AC-2.4: Batches keep being read and written until the newline appears.
    assert copy_characters_in_batches("Hello, world!\nGoodbye", 5) == "Hello"  # First batch before newline
    
    # Test AC-2.5: Nothing beyond the first newline is ever written.
    assert copy_characters_in_batches("This is a test.\nAnd this is another.", 10) == "This is a test."  # Stops at newline
    
    # Test AC-2.6: A batch shorter than requested means the source is exhausted.
    assert copy_characters_in_batches("Short", 10) == "Short"  # Source exhausted before batch completion
    
    # Test AC-2.7: An empty source produces no writes at all.
    assert copy_characters_in_batches("", 5) == ""  # Empty source
    
    # Test AC-2.8: When a batch holds more than one newline, copying is cut at the first.
    assert copy_characters_in_batches("First\nSecond\nThird", 10) == "First"  # Stops at first newline

def test_validate_batch_size():
    # Test AC-3.1: A batch size below 1 is rejected with an error.
    with pytest.raises(ValueError, match="count must be at least 1"):
        validate_batch_size(0)  # Invalid batch size
    
    # Test AC-3.2: A batch size of exactly 1 is accepted.
    assert validate_batch_size(1) == 1  # Valid batch size