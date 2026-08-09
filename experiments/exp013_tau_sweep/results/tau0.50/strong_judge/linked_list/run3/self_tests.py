import pytest
from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1
    assert collection.head is None  # AC-1.1
    assert collection.read_at(0) == []  # AC-1.1

def test_add_to_end_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert collection.size() == 1  # AC-1.2
    assert collection.read_at(0) == 1  # AC-1.2

def test_successive_add_to_end():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.size() == 3  # AC-1.3
    assert collection.read_at(0) == 1  # AC-1.3
    assert collection.read_at(1) == 2  # AC-1.3
    assert collection.read_at(2) == 3  # AC-1.3

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(2)
    collection.add_to_front(1)
    assert collection.size() == 2  # AC-1.4
    assert collection.read_at(0) == 1  # AC-1.4
    assert collection.read_at(1) == 2  # AC-1.4

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
    assert collection.size() == 0  # AC-1.6
    collection.add_to_end(1)
    assert collection.size() == 1  # AC-1.6
    collection.add_to_front(0)
    assert collection.size() == 2  # AC-1.6
    collection.remove_at(1)
    assert collection.size() == 1  # AC-1.6
    collection.remove_at(0)
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
    collection.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.read_at(-1)  # AC-2.2
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.read_at(1)  # AC-2.2
    collection.remove_at(0)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.read_at(0)  # AC-2.2

def test_remove_at():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    assert collection.remove_at(1) == 2  # AC-3.1
    assert collection.size() == 2  # After removal size should be 2
    assert collection.read_at(0) == 1  # AC-3.3
    assert collection.read_at(1) == 3  # AC-3.3

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.remove_at(0)
    assert collection.size() == 1  # AC-3.2
    assert collection.head.value == 2  # AC-3.2

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.remove_at(1)
    assert collection.size() == 1  # AC-3.4
    assert collection.read_at(0) == 1  # AC-3.4

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.remove_at(0)
    assert collection.size() == 0  # AC-3.5
    assert collection.head is None  # AC-3.5

def test_remove_at_out_of_range():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.remove_at(0)  # AC-3.6
    collection.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.remove_at(1)  # AC-3.6
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.remove_at(-1)  # AC-3.6

def test_insert_at_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(3)
    collection.insert_at(1, 2)
    assert collection.size() == 3  # AC-4.2
    assert collection.read_at(0) == 1  # AC-4.2
    assert collection.read_at(1) == 2  # AC-4.2
    assert collection.read_at(2) == 3  # AC-4.2

def test_insert_at_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.insert_at(0, 0)
    assert collection.size() == 2  # AC-4.1
    assert collection.read_at(0) == 0  # AC-4.1
    assert collection.read_at(1) == 1  # AC-4.1

def test_insert_at_end():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.insert_at(1, 2)
    assert collection.size() == 2  # AC-4.3
    assert collection.read_at(0) == 1  # AC-4.3
    assert collection.read_at(1) == 2  # AC-4.3

def test_insert_at_out_of_range():
    collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.insert_at(1, 0)  # AC-4.4
    collection.add_to_end(1)
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.insert_at(2, 0)  # AC-4.4
    with pytest.raises(Exception, match="^index out of bounds$"):
        collection.insert_at(-1, 0)  # AC-4.4

def test_search():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(1)
    assert collection.search(1) == 0  # AC-5.2
    assert collection.search(4) == -1  # AC-5.3

def test_membership():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    assert 1 in collection  # AC-5.1
    assert 2 not in collection  # AC-5.1

def test_reverse():
    collection = SinglyLinkedSequence()
    collection.add_to_end(1)
    collection.add_to_end(2)
    collection.add_to_end(3)
    collection.reverse()
    assert collection.size() == 3  # AC-6.1
    assert collection.read_at(0) == 3  # AC-6.1
    assert collection.read_at(1) == 2  # AC-6.1
    assert collection.read_at(2) == 1  # AC-6.1

def test_reverse_empty_or_single():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.size() == 0  # AC-6.2
    assert collection.head is None  # AC-6.2
    collection.add_to_end(1)
    collection.reverse()
    assert collection.size() == 1  # AC-6.2
    assert collection.head.value == 1  # AC-6.2