import pytest
from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1: Size is zero
    assert collection.head is None  # AC-1.1: No head cell

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert collection.size() == 1  # AC-1.2: Size is 1 after addition
    assert collection.head.value == 1  # AC-1.5: Head cell value is 1

def test_successive_additions():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.size() == 3  # AC-1.3: Size is 3 after additions
    assert collection.head.value == 1  # First added value
    assert collection.head.next.value == 2  # Second added value
    assert collection.head.next.next.value == 3  # Third added value
    assert collection.head.next.next.next is None  # Final cell links to nothing

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(2)
    collection.add_to_front(1)
    assert collection.size() == 2  # AC-1.4: Size is 2
    assert collection.head.value == 1  # AC-1.4: 1 is at the front
    assert collection.head.next.value == 2  # Check next value
    assert collection.head.next.next is None  # Check last cell links to nothing

def test_head_exposes_chain():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.head.value == 1  # AC-1.5: Head value is 1
    assert collection.head.next.value == 2  # AC-1.5: Second cell value is 2
    assert collection.head.next.next.value == 3  # AC-1.5: Third cell value is 3
    assert collection.head.next.next.next is None  # AC-1.5: Final cell links to nothing

def test_size_tracking():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # Initial size
    collection.add_to_end(1)
    assert collection.size() == 1  # Size after addition
    collection.add_to_front(0)
    assert collection.size() == 2  # Size after addition
    collection.remove(0)
    assert collection.size() == 1  # Size after removal
    collection.remove(0)
    assert collection.size() == 0  # Size after removal

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.read(0) == 1  # AC-2.1: Read first element
    assert collection.read(1) == 2  # AC-2.1: Read second element
    assert collection.read(2) == 3  # AC-2.1: Read last element

def test_read_position_out_of_bounds():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="index out of bounds"):
        collection.read(0)  # AC-2.2: Out of bounds error
    collection.add_to_end(1)
    with pytest.raises(Exception, match="index out of bounds"):
        collection.read(1)  # AC-2.2: Out of bounds error
    with pytest.raises(Exception, match="index out of bounds"):
        collection.read(-1)  # AC-2.2: Out of bounds error

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.remove(1) == 2  # AC-3.1: Removed value is 2
    assert collection.size() == 2  # Size after removal
    assert collection.head.value == 1  # First element remains
    assert collection.head.next.value == 3  # Third element comes next

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    assert collection.remove(0) == 1  # AC-3.1: Removed value is 1
    assert collection.size() == 1  # Size is now 1
    assert collection.head.value == 2  # AC-3.2: Head is now 2

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    assert collection.remove(1) == 2  # AC-3.1: Removed value is 2
    assert collection.size() == 1  # Size is now 1
    assert collection.remove(0) == 1  # AC-3.5: Remove last element
    assert collection.size() == 0  # Collection is empty now
    assert collection.head is None  # AC-3.5: No head cell now

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert collection.remove(0) == 1  # AC-3.1: Removed value is 1
    assert collection.size() == 0  # AC-3.5: Collection is empty
    assert collection.head is None  # AC-3.5: No head cell now

def test_remove_out_of_bounds():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="index out of bounds"):
        collection.remove(0)  # AC-3.6: Out of bounds error
    collection.add_to_end(1)
    with pytest.raises(Exception, match="index out of bounds"):
        collection.remove(1)  # AC-3.6: Out of bounds error
    with pytest.raises(Exception, match="index out of bounds"):
        collection.remove(-1)  # AC-3.6: Out of bounds error

def test_insert_at_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(3)
    collection.insert(1, 2)
    assert collection.size() == 3  # Size should be 3 after insert
    assert collection.head.value == 1  # First element
    assert collection.head.next.value == 2  # Inserted element
    assert collection.head.next.next.value == 3  # Last element

def test_insert_at_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(2)
    collection.insert(0, 1)
    assert collection.size() == 2  # Size is 2
    assert collection.head.value == 1  # AC-4.1: Insert at front

def test_insert_at_end():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.insert(1, 2)
    assert collection.size() == 2  # Size is 2
    assert collection.head.value == 1  # First element
    assert collection.head.next.value == 2  # Inserted element

def test_insert_out_of_bounds():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="index out of bounds"):
        collection.insert(1, 1)  # AC-4.4: Out of bounds error
    collection.add_to_end(1)
    with pytest.raises(Exception, match="index out of bounds"):
        collection.insert(2, 2)  # AC-4.4: Out of bounds error
    with pytest.raises(Exception, match="index out of bounds"):
        collection.insert(-1, 2)  # AC-4.4: Out of bounds error

def test_search_value_present():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(1)
    assert collection.search(1) == 0  # AC-5.2: Position of first occurrence of 1

def test_search_value_absent():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    assert collection.search(3) == -1  # AC-5.3: Value not present returns -1

def test_search_membership():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    assert collection.contains(1) is True  # AC-5.1: 1 is present
    assert collection.contains(3) is False  # AC-5.1: 3 is absent

def test_reverse_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    size_before = collection.size()  # Preserve size before reversal
    collection.reverse()
    assert collection.size() == size_before  # AC-6.1: Size is preserved
    assert collection.head.value == 3  # First element should now be 3
    assert collection.head.next.value == 2  # Second element should now be 2
    assert collection.head.next.next.value == 1  # Last element should now be 1
    assert collection.head.next.next.next is None  # Final cell links to nothing

def test_reverse_empty_collection():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.size() == 0  # AC-6.2: Size remains 0
    assert collection.head is None  # Head remains None

def test_reverse_single_element_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.reverse()
    assert collection.size() == 1  # AC-6.2: Size remains 1
    assert collection.head.value == 1  # Single element remains unchanged