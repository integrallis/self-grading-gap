import pytest
from solution import SinglyLinkedSequence

def test_empty_collection():
    s = SinglyLinkedSequence()
    assert s.size() == 0  # AC-1.1: Size is zero
    assert s.to_list() == []  # AC-1.1: Contents is an empty sequence
    assert s.head is None  # AC-1.1: No head cell

def test_add_to_empty_collection():
    s = SinglyLinkedSequence()
    s.add_last(1)
    assert s.size() == 1  # AC-1.2: Size is one after addition
    assert s.to_list() == [1]  # AC-1.2: Contents is [1]

def test_successive_additions():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    s.add_last(3)
    assert s.to_list() == [1, 2, 3]  # AC-1.3: Preserves insertion order

def test_add_to_front():
    s = SinglyLinkedSequence()
    s.add_last(2)
    s.add_front(1)
    assert s.to_list() == [1, 2]  # AC-1.4: Added at front

def test_head_exposes_chain():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    s.add_last(3)
    assert s.head.value == 1  # AC-1.5: Head value is the first element
    assert s.head.next.value == 2  # Next value is the second element
    assert s.head.next.next.value == 3  # Final value is the third element
    assert s.head.next.next.next is None  # Last cell links to nothing

def test_size_tracking():
    s = SinglyLinkedSequence()
    s.add_last(1)
    assert s.size() == 1  # Size should be 1 after first addition
    s.add_front(2)
    assert s.size() == 2  # Size should be 2 after second addition
    s.remove(0)
    assert s.size() == 1  # Size should be 1 after removal

def test_read_position():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    assert s.read(0) == 1  # AC-2.1: First position returns first element
    assert s.read(1) == 2  # AC-2.1: Second position returns second element
    s.add_last(3)
    assert s.read(1) == 2  # AC-2.1: Middle position 1 returns second element
    assert s.read(2) == 3  # AC-2.1: Last position returns last element

def test_out_of_range_read():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.read(2)  # AC-2.2: Out of range error for index 2
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.read(-1)  # AC-2.2: Out of range error for negative index
    s_empty = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        s_empty.read(0)  # AC-2.2: Out of range error for empty collection

def test_remove_element():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    removed_value = s.remove(0)
    assert removed_value == 1  # AC-3.1: Correct value removed
    assert s.to_list() == [2]  # AC-3.2: Second element becomes head
    assert s.size() == 1  # AC-1.6: Size should be 1 after removal

def test_remove_middle_element():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    s.add_last(3)
    removed_value = s.remove(1)
    assert removed_value == 2  # AC-3.1: Correct value removed
    assert s.to_list() == [1, 3]  # AC-3.3: Links former neighbours directly
    assert s.size() == 2  # AC-1.6: Size should be 2 after removal

def test_remove_last_element():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    removed_value = s.remove(1)
    assert removed_value == 2  # AC-3.1: Correct value removed
    assert s.to_list() == [1]  # AC-3.4: Last element removed correctly
    assert s.size() == 1  # AC-1.6: Size should be 1 after removal

def test_remove_only_element():
    s = SinglyLinkedSequence()
    s.add_last(1)
    removed_value = s.remove(0)
    assert removed_value == 1  # AC-3.1: Correct value removed
    assert s.size() == 0  # AC-3.5: Collection is empty
    assert s.head is None  # No head after removal

def test_out_of_range_remove():
    s = SinglyLinkedSequence()
    s.add_last(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.remove(1)  # AC-3.6: Out of range error for index 1
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.remove(-1)  # AC-3.6: Out of range error for negative index
    s.remove(0)  # Remove existing element
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.remove(0)  # AC-3.6: Out of range error for removing from empty collection

def test_insert_at_position_zero():
    s = SinglyLinkedSequence()
    s.insert(0, 1)  # Insert into empty collection
    assert s.to_list() == [1]  # AC-4.1: Insert at front
    assert s.size() == 1  # Size should be 1 after insertion

def test_insert_middle_position():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(3)
    s.insert(1, 2)
    assert s.to_list() == [1, 2, 3]  # AC-4.2: Middle insert shifts elements
    assert s.size() == 3  # Size should be 3 after insertion

def test_insert_at_end():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.insert(1, 2)  # Insert at size
    assert s.to_list() == [1, 2]  # AC-4.3: Insert at end
    assert s.size() == 2  # Size should be 2 after insertion

def test_out_of_range_insert():
    s = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.insert(1, 1)  # AC-4.4: Out of range error for index 1
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.insert(-1, 1)  # AC-4.4: Out of range error for negative index
    s.add_last(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        s.insert(2, 2)  # AC-4.4: Out of range error for index equal to size

def test_membership_search():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    assert s.contains(1) is True  # AC-5.1: Membership is true for stored value
    assert s.contains(3) is False  # AC-5.1: Membership is false for absent value

def test_search_position():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    s.add_last(1)
    assert s.position_of(1) == 0  # AC-5.2: First occurrence position
    assert s.position_of(2) == 1  # AC-5.2: Second occurrence position
    assert s.position_of(3) == -1  # AC-5.3: Absent value position
    assert s.position_of(1) == 0  # Check for first occurrence at position 0
    s.add_last(3)
    assert s.position_of(3) == 2  # Check for first occurrence at last position

def test_reverse():
    s = SinglyLinkedSequence()
    s.add_last(1)
    s.add_last(2)
    s.add_last(3)
    original_head = s.head  # Capture original head cell
    s.reverse()
    assert s.to_list() == [3, 2, 1]  # AC-6.1: Order reversed
    assert s.size() == 3  # AC-6.1: Size remains the same
    assert s.head is original_head.next.next  # Check if the original last is now the head

def test_reverse_empty_or_single():
    s_empty = SinglyLinkedSequence()
    s_empty.reverse()
    assert s_empty.to_list() == []  # AC-6.2: Empty remains unchanged

    s_single = SinglyLinkedSequence()
    s_single.add_last(1)
    s_single.reverse()
    assert s_single.to_list() == [1]  # AC-6.2: Single element remains unchanged