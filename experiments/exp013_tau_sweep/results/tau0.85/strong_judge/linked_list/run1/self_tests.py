import pytest
from solution import *

def test_empty_collection():
    # A brand-new collection is empty: its size is zero, its contents read back as an empty sequence, and it has no head cell.
    seq = SinglyLinkedSequence()
    assert seq.size() == 0  # size should be 0
    assert seq.to_list() == []  # contents should be an empty sequence
    assert seq.head is None  # head should be None

def test_add_to_empty_collection():
    # Adding to the end of an empty collection yields a one-element collection.
    seq = SinglyLinkedSequence()
    seq.add_last(1)  # add element 1
    assert seq.size() == 1  # size should be 1
    assert seq.to_list() == [1]  # contents should be [1]

def test_successive_additions_preserve_order():
    # Successive additions at the end preserve insertion order.
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(3)
    assert seq.to_list() == [1, 2, 3]  # contents should be [1, 2, 3]

def test_add_front():
    # An element can be added at the front, taking its place before all existing elements.
    seq = SinglyLinkedSequence()
    seq.add_last(2)
    seq.add_front(1)  # add element 1 at the front
    assert seq.to_list() == [1, 2]  # contents should be [1, 2]

def test_head_exposes_chain():
    # The head exposes the chain of cells: each cell carries its value and a link to the next cell, and the final cell links to nothing.
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    head = seq.head
    assert head.value == 1  # head should be 1
    assert head.next.value == 2  # next should be 2
    assert head.next.next is None  # final cell should link to nothing

def test_size_tracking():
    # The reported size tracks every addition — at either end — and every removal.
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_front(0)
    assert seq.size() == 2  # size should be 2
    seq.remove(0)  # remove first element
    assert seq.size() == 1  # size should be 1
    seq.remove(0)  # remove last element
    assert seq.size() == 0  # size should be 0

def test_reading_position():
    # Positions count from zero, and every position from the first to the last element can be read.
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    assert seq.get(0) == 1  # first position should be 1
    assert seq.get(1) == 2  # second position should be 2

def test_out_of_range_reading():
    # Reading a position outside the range zero to size minus one — including any position of an empty collection — is refused with an out-of-range error carrying the message "index out of bounds".
    seq = SinglyLinkedSequence()
    with pytest.raises(Exception) as e:
        seq.get(0)  # reading from empty should raise error
    assert str(e.value) == "index out of bounds"

    seq.add_last(1)
    with pytest.raises(Exception) as e:
        seq.get(1)  # reading out of bounds should raise error
    assert str(e.value) == "index out of bounds"

    with pytest.raises(Exception) as e:
        seq.get(-1)  # negative index should raise error
    assert str(e.value) == "index out of bounds"

def test_removal():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(3)
    assert seq.remove(1) == 2  # remove at position 1 should return 2
    assert seq.to_list() == [1, 3]  # contents should be [1, 3]

def test_remove_first_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.remove(0)  # remove first element
    assert seq.to_list() == [2]  # contents should be [2]

def test_remove_middle_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(3)
    seq.remove(1)  # remove middle element
    assert seq.to_list() == [1, 3]  # contents should be [1, 3]
    assert seq.size() == 2  # size should be 2 after removal

def test_remove_last_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.remove(1)  # remove last element
    assert seq.to_list() == [1]  # contents should be [1]
    assert seq.size() == 1  # size should be 1 after removal

def test_remove_only_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.remove(0)  # remove only element
    assert seq.size() == 0  # size should be 0
    assert seq.head is None  # head should be None

def test_out_of_range_removal():
    # Removing at a position outside the range zero to size minus one — including from an empty collection — is refused with an out-of-range error carrying the message "index out of bounds".
    seq = SinglyLinkedSequence()
    with pytest.raises(Exception) as e:
        seq.remove(0)  # removing from empty should raise error
    assert str(e.value) == "index out of bounds"

    seq.add_last(1)
    with pytest.raises(Exception) as e:
        seq.remove(1)  # removing out of bounds should raise error
    assert str(e.value) == "index out of bounds"

    with pytest.raises(Exception) as e:
        seq.remove(-1)  # negative index should raise error
    assert str(e.value) == "index out of bounds"

def test_inserting_at_position_zero():
    seq = SinglyLinkedSequence()
    seq.insert(0, 1)  # insert at position 0 into empty sequence
    assert seq.to_list() == [1]  # contents should be [1]

def test_inserting_in_middle_position():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(3)
    seq.insert(1, 2)  # insert 2 at position 1
    assert seq.to_list() == [1, 2, 3]  # contents should be [1, 2, 3]
    assert seq.size() == 3  # size should be 3 after insertion

def test_inserting_at_end_position():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.insert(2, 3)  # insert 3 at the end
    assert seq.to_list() == [1, 2, 3]  # contents should be [1, 2, 3]

def test_out_of_range_insertion():
    seq = SinglyLinkedSequence()
    with pytest.raises(Exception) as e:
        seq.insert(1, 1)  # inserting out of bounds should raise error
    assert str(e.value) == "index out of bounds"

    seq.add_last(1)
    with pytest.raises(Exception) as e:
        seq.insert(2, 2)  # inserting out of bounds should raise error
    assert str(e.value) == "index out of bounds"

    with pytest.raises(Exception) as e:
        seq.insert(-1, 1)  # negative index should raise error
    assert str(e.value) == "index out of bounds"

def test_search_membership():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    assert seq.contains(1) == True  # should return True for stored value
    assert seq.contains(3) == False  # should return False for absent value

def test_search_position():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.add_last(1)
    assert seq.index_of(1) == 0  # first occurrence of 1 should be at index 0
    assert seq.index_of(2) == 1  # first occurrence of 2 should be at index 1
    assert seq.index_of(3) == -1  # absent value should return -1

def test_reverse():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    seq.reverse()
    assert seq.to_list() == [2, 1]  # contents should be [2, 1]

def test_reverse_empty():
    seq = SinglyLinkedSequence()
    seq.reverse()
    assert seq.to_list() == []  # contents should still be []

def test_reverse_single_element():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.reverse()
    assert seq.to_list() == [1]  # contents should still be [1]

def test_reverse_size_preservation():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    size_before = seq.size()
    seq.reverse()
    assert seq.size() == size_before  # size should remain the same after reversal

def test_reverse_cell_identity():
    seq = SinglyLinkedSequence()
    seq.add_last(1)
    seq.add_last(2)
    head_before = seq.head
    second_before = head_before.next
    seq.reverse()
    assert seq.head == second_before  # new head should be the former second element
    assert seq.head.next == head_before  # new second should be the former head