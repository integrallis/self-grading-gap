from solution import copy_characters

def test_copy_one_character_at_a_time():
    # AC-1.1
    source = "Hello\nWorld"
    destination = []
    copy_characters(source, destination)
    assert destination == ['H', 'e', 'l', 'l', 'o']  # First line copied

    # AC-1.2
    source = "\nWorld"
    destination = []
    copy_characters(source, destination)
    assert destination == []  # No characters written
    
    # AC-1.3
    source = "Hello\nWorld"
    destination = []
    copy_characters(source, destination)
    assert destination[-1] != '\n'  # Last character is not a newline
    
    # AC-1.4
    source = "Hello\nWorld"
    destination = []
    copy_characters(source, destination)
    assert 'W' not in destination  # No content after newline copied
    
    # AC-1.5
    source = "Hello\nWorld"
    destination = []
    copy_characters(source, destination)
    assert destination == ['H', 'e', 'l', 'l', 'o']  # Stops after newline
    
    # AC-1.6
    source = "Hello"  # No newline
    destination = []
    copy_characters(source, destination)
    assert destination == ['H', 'e', 'l', 'l', 'o']  # All characters copied
    
    # AC-1.7
    source = "Hello, World!"
    destination = []
    copy_characters(source, destination)
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!']  # All characters copied

def test_copy_in_batches():
    # AC-2.1
    source = "Hello, World\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=13)  # Batch size includes the newline
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd']  # Batch written without newline
    
    # AC-2.2
    source = "Hello, World\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=15)  # Batch size exceeds the length before newline
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd']  # Same as above
    
    # AC-2.3
    source = "\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=5)
    assert destination == []  # No characters written
    
    # AC-2.4
    source = "Hello, World\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=5)  # Batches of 5
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd']  # All copied until newline
    
    # AC-2.5
    source = "Hello, World\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=8)  # Batch size includes newline
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W']  # Stops at first newline
    
    # AC-2.6
    source = "Hello"
    destination = []
    copy_characters(source, destination, batch_size=10)  # Batch size exceeds length
    assert destination == ['H', 'e', 'l', 'l', 'o']  # All characters copied
    
    # AC-2.7
    source = ""
    destination = []
    copy_characters(source, destination, batch_size=5)
    assert destination == []  # Empty source produces no writes
    
    # AC-2.8
    source = "Hello\nWorld\nAgain"
    destination = []
    copy_characters(source, destination, batch_size=10)  # Batch contains multiple newlines
    assert destination == ['H', 'e', 'l', 'l', 'o']  # Stops at first newline

def test_batch_size_validation():
    # AC-3.1
    import pytest
    with pytest.raises(ValueError, match="count must be at least 1"):
        copy_characters("Hello", [], batch_size=0)  # Batch size below 1
    
    # AC-3.2
    source = "Hello, World\nNext line"
    destination = []
    copy_characters(source, destination, batch_size=1)  # Batch size of exactly 1
    assert destination == ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd']  # One character copied at a time