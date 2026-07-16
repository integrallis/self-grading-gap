import pytest
from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1: size is zero
    assert collection.head() is None  # AC-1.1: no head cell
    assert collection.to_list() == []  # AC-1.1: contents read back as an empty sequence

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    assert collection.size() == 1  # AC-1.2: size is one
    assert collection.to_list() == [1]  # AC-1.2: contents is [1]

def test_successive_additions_at_end():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.to_list() == [1, 2, 3]  # AC-1.3: maintains order

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_end(2)
    collection.add_end(3)
    collection.add_front(1)
    assert collection.to_list() == [1, 2, 3]  # AC-1.4: add at front

def test_head_exposes_chain_of_cells():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    head = collection.head()
    assert head.value == 1  # AC-1.5: head cell value
    assert head.next.value == 2  # AC-1.5: second cell value
    assert head.next.next.value == 3  # AC-1.5: third cell value
    assert head.next.next.next is None  # AC-1.5: last cell links to nothing

def test_size_tracks_additions_and_removals():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # initial size
    collection.add_end(1)
    assert collection.size() == 1  # size after addition
    collection.add_end(2)
    assert collection.size() == 2  # size after addition
    collection.remove(0)
    assert collection.size() == 1  # size after removal
    collection.remove(0)
    assert collection.size() == 0  # size after removal

def test_add_front_updates_size():
    collection = SinglyLinkedSequence()
    collection.add_front(1)
    assert collection.size() == 1  # size after adding front

def test_positional_access():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.get(0) == 1  # AC-2.1: first element
    assert collection.get(1) == 2  # AC-2.1: second element
    assert collection.get(2) == 3  # AC-2.1: third element

def test_out_of_bounds_reading():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.get(2)  # AC-2.2: out of bounds
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.get(-1)  # AC-2.2: out of bounds
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        empty_collection.get(0)  # AC-2.2: out of bounds on empty

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    removed_value = collection.remove(1)
    assert removed_value == 2  # AC-3.1: value removed
    assert collection.to_list() == [1, 3]  # AC-3.3: correct linking after removal

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.remove(0)
    assert collection.to_list() == [2]  # AC-3.2: head promoted correctly

def test_remove_middle_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    collection.remove(1)
    assert collection.to_list() == [1, 3]  # AC-3.3: middle element removal

def test_remove_final_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    collection.remove(2)  # Remove the final element (index 2)
    assert collection.to_list() == [1, 2]  # Remaining should be [1, 2]

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.remove(0)
    assert collection.size() == 0  # AC-3.5: empty collection
    assert collection.head() is None  # AC-3.5: no head

def test_out_of_bounds_removal():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.remove(1)  # AC-3.6: out of bounds
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.remove(-1)  # AC-3.6: out of bounds
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        empty_collection.remove(0)  # AC-3.6: out of bounds on empty

def test_insert_at_position_zero():
    collection = SinglyLinkedSequence()
    collection.insert(0, 1)  # Inserting into an empty collection
    assert collection.to_list() == [1]  # Should produce [1]
    assert collection.size() == 1  # Size should be one

def test_insert_at_middle_position():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(3)
    collection.insert(1, 2)
    assert collection.to_list() == [1, 2, 3]  # AC-4.2: insert in middle
    assert collection.size() == 3  # Size should increase

def test_insert_at_end_position():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.insert(2, 3)
    assert collection.to_list() == [1, 2, 3]  # AC-4.3: insert at end

def test_out_of_bounds_insertion():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.insert(2, 2)  # AC-4.4: out of bounds
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.insert(-1, 2)  # AC-4.4: out of bounds
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        empty_collection.insert(1, 2)  # AC-4.4: out of bounds on empty

def test_search_existing_value():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(1)
    assert collection.search(1) == 0  # AC-5.2: first occurrence of 1

def test_search_non_existing_value():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    assert collection.search(3) == -1  # AC-5.3: absent value returns -1

def test_search_value_membership():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    assert collection.contains(1) is True  # AC-5.1: membership true
    assert collection.contains(3) is False  # AC-5.1: membership false

def test_reverse_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    collection.reverse()
    assert collection.to_list() == [3, 2, 1]  # AC-6.1: reversed order
    assert collection.size() == 3  # Size should remain unchanged

def test_reverse_empty_collection():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.to_list() == []  # AC-6.2: unchanged

def test_reverse_single_element_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.reverse()
    assert collection.to_list() == [1]  # AC-6.2: unchanged

def test_insert_at_zero_with_existing_elements():
    collection = SinglyLinkedSequence()
    collection.add_end(2)
    collection.add_end(3)
    collection.insert(0, 1)
    assert collection.to_list() == [1, 2, 3]  # Inserting at zero should place 1 before existing values

def test_search_value_at_nonzero_index():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(1)
    assert collection.search(2) == 1  # First occurrence of 2 is at index 1