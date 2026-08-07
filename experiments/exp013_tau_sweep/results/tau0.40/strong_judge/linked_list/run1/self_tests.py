import pytest
from solution import SinglyLinkedSequence  # Replace with the actual class name as necessary

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1
    assert collection.to_list() == []  # AC-1.1
    assert collection.head is None  # AC-1.1

def test_add_to_end_empty():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert collection.size() == 1  # AC-1.2
    assert collection.to_list() == [1]  # AC-1.2

def test_add_to_end_preserves_order():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.to_list() == [1, 2, 3]  # AC-1.3

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(2)
    collection.add_to_front(1)
    assert collection.to_list() == [1, 2]  # AC-1.4
    assert collection.size() == 2  # AC-1.6

def test_head_exposes_chain():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.head.value == 1  # AC-1.5
    assert collection.head.next.value == 2  # AC-1.5
    assert collection.head.next.next.value == 3  # AC-1.5
    assert collection.head.next.next.next is None  # AC-1.5

def test_size_tracks_additions_removals():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.remove_at(0)  # Should remove 1
    assert collection.size() == 1  # AC-1.6
    collection.remove_at(0)  # Should remove 2
    assert collection.size() == 0  # AC-1.6

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.read_at(0) == 1  # AC-2.1
    assert collection.read_at(1) == 2  # AC-2.1
    assert collection.read_at(2) == 3  # AC-2.1

def test_read_position_out_of_range():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-2.2
        collection.read_at(0)  # From empty collection
    collection.add_to_end(1)
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-2.2
        collection.read_at(1)  # Out of range
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-2.2
        collection.read_at(-1)  # Negative index

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.remove_at(1) == 2  # AC-3.1
    assert collection.to_list() == [1, 3]  # AC-3.1
    assert collection.size() == 2  # AC-1.6

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.remove_at(0)  # Removes 1
    assert collection.head.value == 2  # AC-3.2
    assert collection.size() == 1  # AC-3.2

def test_remove_middle_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    collection.remove_at(1)  # Remove 2
    assert collection.to_list() == [1, 3]  # AC-3.3
    assert collection.size() == 2  # AC-1.6

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.remove_at(1)  # Remove 2
    assert collection.to_list() == [1]  # AC-3.4
    assert collection.size() == 1  # AC-1.6

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.remove_at(0)  # Remove 1
    assert collection.size() == 0  # AC-3.5
    assert collection.head is None  # AC-3.5

def test_remove_out_of_range():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-3.6
        collection.remove_at(0)  # From empty collection
    collection.add_to_end(1)
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-3.6
        collection.remove_at(1)  # Out of range
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-3.6
        collection.remove_at(-1)  # Negative index

def test_insert_at_position_zero():
    collection = SinglyLinkedSequence()
    collection.insert_at(0, 1)  # Insert into empty collection
    assert collection.to_list() == [1]  # AC-4.1
    assert collection.size() == 1  # AC-1.6

def test_insert_at_middle_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(3)
    collection.insert_at(1, 2)  # Insert 2 at position 1
    assert collection.to_list() == [1, 2, 3]  # AC-4.2
    assert collection.size() == 3  # AC-1.6

def test_insert_at_end_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.insert_at(2, 3)  # Insert 3 at end
    assert collection.to_list() == [1, 2, 3]  # AC-4.3
    assert collection.size() == 3  # AC-1.6

def test_insert_out_of_range():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-4.4
        collection.insert_at(1, 1)  # Invalid position on empty collection
    collection.add_to_end(1)
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-4.4
        collection.insert_at(2, 2)  # Out of range
    with pytest.raises(Exception, match=r"^index out of bounds$"):  # AC-4.4
        collection.insert_at(-1, 2)  # Negative index

def test_search_found():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.search(2) == 1  # AC-5.2

def test_search_not_found():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    assert collection.search(3) == -1  # AC-5.3

def test_membership_true():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert (1 in collection) is True  # AC-5.1

def test_membership_false():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert (2 in collection) is False  # AC-5.1

def test_search_duplicates():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(1)
    assert collection.search(1) == 0  # AC-5.2

def test_reverse():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    collection.reverse()
    assert collection.to_list() == [3, 2, 1]  # AC-6.1
    assert collection.size() == 3  # AC-6.1

def test_reverse_empty():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.size() == 0  # AC-6.2
    assert collection.to_list() == []  # AC-6.2

def test_reverse_single_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.reverse()
    assert collection.size() == 1  # AC-6.2
    assert collection.to_list() == [1]  # AC-6.2