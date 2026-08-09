from solution import SinglyLinkedSequence
import pytest

def test_empty_collection():
    sequence = SinglyLinkedSequence()
    assert sequence.size() == 0  # AC-1.1: size is zero
    assert sequence.head is None  # AC-1.1: no head cell

def test_add_to_empty_collection():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(5)
    assert sequence.size() == 1  # AC-1.2: size is now one
    assert sequence.head.value == 5  # AC-1.2: head value is 5

def test_successive_additions():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    sequence.add_to_end(3)
    assert sequence.size() == 3  # Ensure size is 3
    assert sequence.head.value == 1  # The head value should be 1
    assert sequence.head.next.value == 2  # The second cell value should be 2
    assert sequence.head.next.next.value == 3  # The third cell value should be 3

def test_add_to_front():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_front(0)
    assert sequence.size() == 2  # Size should be updated after adding to front
    assert sequence.head.value == 0  # AC-1.4: added 0 at front

def test_head_exposes_chain():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    assert sequence.head.value == 1  # AC-1.5: head cell value is 1
    assert sequence.head.next.value == 2  # AC-1.5: second cell value is 2
    assert sequence.head.next.next is None  # AC-1.5: final cell links to nothing

def test_size_tracks_additions_and_removals():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    assert sequence.size() == 2  # Size should be 2 after two additions
    sequence.remove_at(0)
    assert sequence.size() == 1  # AC-1.6: size is 1 after removal

def test_reading_valid_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    assert sequence.read_at(0) == 1  # AC-2.1: first position returns 1
    assert sequence.read_at(1) == 2  # AC-2.1: second position returns 2

def test_reading_out_of_range_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.read_at(2)  # AC-2.2: out of range
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.read_at(-1)  # AC-2.2: negative index
    sequence_empty = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence_empty.read_at(0)  # AC-2.2: empty collection

def test_remove_first_element():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    removed_value = sequence.remove_at(0)
    assert removed_value == 1  # AC-3.1: removed value is 1
    assert sequence.head.value == 2  # AC-3.2: head is now 2

def test_remove_middle_element():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    sequence.add_to_end(3)
    removed_value = sequence.remove_at(1)
    assert removed_value == 2  # AC-3.1: removed value is 2
    assert sequence.head.value == 1  # Head should still be 1
    assert sequence.head.next.value == 3  # AC-3.3: links correctly

def test_remove_last_element():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    removed_value = sequence.remove_at(1)
    assert removed_value == 2  # AC-3.1: removed value is 2
    assert sequence.size() == 1  # AC-3.4: size is now 1
    assert sequence.head.value == 1  # Remaining sequence is intact

def test_remove_only_element():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    removed_value = sequence.remove_at(0)
    assert removed_value == 1  # AC-3.1: removed value is 1
    assert sequence.size() == 0  # AC-3.5: size is now 0
    assert sequence.head is None  # AC-3.5: no head

def test_remove_out_of_range_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.remove_at(1)  # AC-3.6: out of range
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.remove_at(-1)  # AC-3.6: negative index
    sequence_empty = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence_empty.remove_at(0)  # AC-3.6: empty collection

def test_insert_at_position_zero():
    sequence = SinglyLinkedSequence()
    sequence.insert_at(0, 1)  # AC-4.1: insert at front
    assert sequence.size() == 1  # Size should be 1 after insertion
    assert sequence.head.value == 1  # The only element should be 1

def test_insert_at_middle_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(3)
    sequence.insert_at(1, 2)  # AC-4.2: insert in middle
    assert sequence.head.value == 1  # Head should be 1
    assert sequence.head.next.value == 2  # Second element should be 2
    assert sequence.head.next.next.value == 3  # Third element should be 3
    assert sequence.size() == 3  # Size should increase by 1

def test_insert_at_end_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.insert_at(1, 2)  # AC-4.3: insert at end
    assert sequence.head.value == 1  # Head should be 1
    assert sequence.head.next.value == 2  # Second element should be 2
    assert sequence.size() == 2  # Size should be updated after appending

def test_insert_out_of_range_position():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.insert_at(2, 2)  # AC-4.4: out of range
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence.insert_at(-1, 2)  # AC-4.4: negative index
    sequence_empty = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        sequence_empty.insert_at(1, 1)  # AC-4.4: empty collection

def test_search_existing_value():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    sequence.add_to_end(2)
    assert sequence.search(1) == 0  # AC-5.2: first occurrence of 1 is at index 0
    assert sequence.search(2) == 1  # AC-5.2: first occurrence of 2 is at index 1

def test_search_non_existent_value():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    assert sequence.search(2) == -1  # AC-5.3: 2 is not in the collection

def test_search_value_membership():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    assert sequence.contains(1) is True  # AC-5.1: 1 is in the collection
    assert sequence.contains(2) is False  # AC-5.1: 2 is not in the collection

def test_reverse_collection():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.add_to_end(2)
    sequence.add_to_end(3)
    sequence.reverse()
    assert sequence.head.value == 3  # New head should be 3
    assert sequence.head.next.value == 2  # Second element should be 2
    assert sequence.head.next.next.value == 1  # Last element should be 1
    assert sequence.size() == 3  # Reversal should preserve size

def test_reverse_empty_collection():
    sequence = SinglyLinkedSequence()
    sequence.reverse()
    assert sequence.size() == 0  # AC-6.2: remains empty

def test_reverse_single_element_collection():
    sequence = SinglyLinkedSequence()
    sequence.add_to_end(1)
    sequence.reverse()
    assert sequence.head.value == 1  # AC-6.2: remains unchanged
    assert sequence.size() == 1  # Size should still be 1