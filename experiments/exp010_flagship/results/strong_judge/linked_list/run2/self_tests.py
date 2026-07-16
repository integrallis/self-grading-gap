from solution import SinglyLinkedSequence
import pytest

def test_empty_collection_properties():
    seq = SinglyLinkedSequence()
    assert seq.size() == 0  # AC-1.1: The size should be zero
    assert seq.head() is None  # AC-1.1: The head should be None
    assert seq.to_list() == []  # AC-1.1: The contents should be an empty sequence

def test_add_to_empty_collection():
    seq = SinglyLinkedSequence()
    seq.add_last(1)  # AC-1.2: Adding to the end of an empty collection
    assert seq.size() == 1  # Size should be 1
    assert seq.to_list() == [1]  # Contents should be [1]

def test_successive_additions_preserve_order():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(3)  # AC-1.3: Successive additions should preserve order
    assert seq.to_list() == [1, 2, 3]  # Contents should be [1, 2, 3]

def test_add_to_front():
    seq = SinglyLinkedSequence()
    seq.add_last(2)
    seq.add_first(1)  # AC-1.4: Adding to the front
    assert seq.to_list() == [1, 2]  # Contents should be [1, 2]

def test_head_cell_exposes_chain():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    head = seq.head()  # Get the head cell
    assert head.value == 1  # AC-1.5: Head should expose first element
    assert head.next.value == 2  # Next should expose second element
    assert head.next.next is None  # Final cell should link to nothing

def test_size_tracks_additions_and_removals():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    assert seq.size() == 2  # Size should be 2
    seq.remove(0)
    assert seq.size() == 1  # Size should be 1 after removal
    seq.remove(0)
    assert seq.size() == 0  # Size should be 0 after all removals
    seq.add_first(1)  # Adding to front
    assert seq.size() == 1  # Size should be 1 after addition

def test_access_valid_positions():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    assert seq.get(0) == 1  # AC-2.1: Get first element
    assert seq.get(1) == 2  # AC-2.1: Get second element

def test_access_out_of_bounds():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.get(2)  # AC-2.2: Accessing out of bounds
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.get(-1)  # AC-2.2: Accessing negative index
    empty_seq = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        empty_seq.get(0)  # AC-2.2: Accessing from empty collection

def test_remove_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    value = seq.remove(0)  # AC-3.1: Removing first element
    assert value == 1  # Should return the removed value
    assert seq.to_list() == [2]  # Remaining elements should be [2]

def test_remove_first_element_promotes_second():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.remove(0)  # AC-3.2: Removing first element
    assert seq.head().value == 2  # Head should now be the second element

def test_remove_middle_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(3)
    seq.remove(1)  # AC-3.3: Removing middle element
    assert seq.to_list() == [1, 3]  # Remaining elements should be [1, 3]
    assert seq.size() == 2  # Size should be 2 after removal

def test_remove_last_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.remove(1)  # AC-3.4: Removing last element
    assert seq.to_list() == [1]  # Remaining elements should be [1]
    assert seq.size() == 1  # Size should be 1 after removal

def test_remove_only_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.remove(0)  # AC-3.5: Removing the only element
    assert seq.size() == 0  # Size should be 0
    assert seq.head() is None  # Head should be None

def test_remove_out_of_bounds():
    seq = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.remove(0)  # AC-3.6: Removing from empty collection
    seq.add_last(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.remove(1)  # AC-3.6: Removing at index equal to size
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.remove(-1)  # AC-3.6: Removing at negative index

def test_insert_at_start():
    seq = SinglyLinkedSequence()
    seq.insert(0, 1)  # AC-4.1: Inserting at position 0 into empty sequence
    assert seq.to_list() == [1]  # Contents should be [1]
    assert seq.size() == 1  # Size should be 1

def test_insert_at_middle():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(3)
    seq.insert(1, 2)  # AC-4.2: Inserting in the middle
    assert seq.to_list() == [1, 2, 3]  # Contents should be [1, 2, 3]
    assert seq.size() == 3  # Size should be 3 after insertion

def test_insert_at_end():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.insert(1, 2)  # AC-4.3: Inserting at size (end)
    assert seq.to_list() == [1, 2]  # Contents should be [1, 2]
    assert seq.size() == 2  # Size should be 2 after insertion

def test_insert_out_of_bounds():
    seq = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.insert(-1, 2)  # AC-4.4: Inserting at negative index
    with pytest.raises(Exception, match="^index out of bounds$"):
        seq.insert(1, 2)  # AC-4.4: Inserting at index greater than size

def test_membership():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    assert seq.contains(1)  # AC-5.1: Membership check for stored value
    assert not seq.contains(3)  # AC-5.1: Membership check for absent value
    assert not seq.contains(0)  # Membership check for absent value in empty collection

def test_first_occurrence_position():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(1)
    assert seq.index(1) == 0  # AC-5.2: Position of first occurrence
    assert seq.index(2) == 1  # Position of second element
    assert seq.index(3) == -1  # AC-5.3: Position of absent value

def test_reverse_collection():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.reverse()  # AC-6.1: Reverse the collection
    assert seq.to_list() == [2, 1]  # Contents should be [2, 1]
    assert seq.size() == 2  # Size should still be 2

def test_reverse_empty_or_single_element():
    seq_empty = SinglyLinkedSequence()
    seq_empty.reverse()  # AC-6.2: Reverse empty collection
    assert seq_empty.to_list() == []  # Should remain empty

    seq_single = SinglyLinkedSequence()
    seq_single.add_last(1)
    seq_single.reverse()  # AC-6.2: Reverse single element
    assert seq_single.to_list() == [1]  # Should remain [1]