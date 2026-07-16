from solution import copy_one_character_at_a_time, copy_in_batches

def test_copy_one_character_at_a_time():
    # AC-1.1
    result = copy_one_character_at_a_time("Hello\nWorld")
    assert result == "Hello"  # "Hello" comes before the newline

    # AC-1.2
    result = copy_one_character_at_a_time("\nWorld")
    assert result == ""  # Nothing is written since the first character is a newline

    # AC-1.3
    result = copy_one_character_at_a_time("Hello\n")
    assert result == "Hello"  # Newline is not written

    # AC-1.4
    result = copy_one_character_at_a_time("Hello World\nGoodbye")
    assert result == "Hello World"  # Content after the newline is not copied

    # AC-1.5
    result = copy_one_character_at_a_time("Hello\nWorld")
    assert result == "Hello"  # Stops reading after the newline

    # AC-1.6
    result = copy_one_character_at_a_time("Hello World")
    assert result == "Hello World"  # Source runs out before newline, everything written

    # AC-1.7
    result = copy_one_character_at_a_time("Hello, World!\n")
    assert result == "Hello, World!"  # Ordinary characters are copied verbatim

def test_copy_in_batches():
    # AC-2.1
    result = copy_in_batches("Hello, World!", 5)
    assert result == "Hello"  # Batch written whole since no newline in the batch

    # AC-2.2
    result = copy_in_batches("Hello, World!\nGoodbye", 10)
    assert result == "Hello, World!"  # Batch written only up to newline

    # AC-2.3
    result = copy_in_batches("\nHello, World!", 5)
    assert result == ""  # Source begins with newline, produces no writes

    # AC-2.4
    result = copy_in_batches("Hello, World!\nGoodbye, Universe!", 5)
    assert result == "Hello"  # Multiple batches read until newline

    # AC-2.5
    result = copy_in_batches("Hello,\nWorld!\nGoodbye!", 7)
    assert result == "Hello,"  # Stops copying at the first newline

    # AC-2.6
    result = copy_in_batches("Hello", 10)
    assert result == "Hello"  # Shorter batch than requested means source exhausted

    # AC-2.7
    result = copy_in_batches("", 5)
    assert result == ""  # Empty source produces no writes

    # AC-2.8
    result = copy_in_batches("Hello,\nWorld!\nGoodbye!", 10)
    assert result == "Hello,"  # Stops at first newline

def test_batch_size_validation():
    # AC-3.1
    import pytest
    with pytest.raises(ValueError, match="count must be at least 1"):
        copy_in_batches("Hello, World!", 0)  # Batch size below 1

    # AC-3.2
    result = copy_in_batches("Hello\nWorld", 1)
    assert result == "H"  # Batch size of exactly 1 copies one character