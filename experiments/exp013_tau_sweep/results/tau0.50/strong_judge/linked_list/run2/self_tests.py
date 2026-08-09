import pytest
from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1
    assert collection.head is None  # AC-1.1
    assert collection.contents() == []  # AC-1.1: verify contents is an empty sequence

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)  # Adding an element
    assert collection.size() == 1  # AC-1.2
    assert collection.head.value == 10  # Verify head value for AC-1.2
    assert collection.contents() == [10]  # Verify contents for AC-1.2

def test_successive_additions():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.size() == 3  # AC-1.3
    assert collection.head.value == 10  # Verify head value for AC-1.3
    assert collection.head.next.value == 20  # Verify second value for AC-1.3
    assert collection.head.next.next.value == 30  # Verify third value for AC-1.3
    assert collection.contents() == [10, 20, 30]  # Verify contents for AC-1.3

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(20)
    collection.add_to_front(10)
    assert collection.head.value == 10  # Verify head value for AC-1.4
    assert collection.head.next.value == 20  # Verify next value for AC-1.4
    assert collection.contents() == [10, 20]  # Verify contents for AC-1.4

def test_head_exposes_chain():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.head.value == 10  # AC-1.5
    assert collection.head.next.value == 20  # AC-1.5
    assert collection.head.next.next.value == 30  # AC-1.5
    assert collection.head.next.next.next is None  # AC-1.5

def test_size_tracking():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.remove_at(0)  # Removes 10
    assert collection.size() == 1  # AC-1.6
    collection.add_to_front(30)
    assert collection.size() == 2  # AC-1.6
    collection.remove_at(1)  # Removes 20
    assert collection.size() == 1  # AC-1.6
    collection.remove_at(0)  # Removes 30
    assert collection.size() == 0  # AC-1.6

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.read_at(0) == 10  # AC-2.1
    assert collection.read_at(1) == 20  # AC-2.1
    assert collection.read_at(2) == 30  # AC-2.1

def test_read_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.read_at(3)  # AC-2.2
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.read_at(-1)  # AC-2.2
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        empty_collection.read_at(0)  # AC-2.2 on empty collection

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.remove_at(1) == 20  # AC-3.1
    assert collection.head.next.value == 30  # Check remaining elements for AC-3.1
    assert collection.size() == 2  # AC-3.1

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.remove_at(0)  # Removes 10
    assert collection.head.value == 20  # AC-3.2
    assert collection.contents() == [20]  # Verify contents for AC-3.2

def test_remove_middle_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    collection.remove_at(1)  # Removes 20
    assert collection.head.value == 10  # Check head for AC-3.3
    assert collection.head.next.value == 30  # Check next for AC-3.3
    assert collection.contents() == [10, 30]  # Verify contents for AC-3.3

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.remove_at(1)  # Removes 20
    assert collection.head.value == 10  # Check remaining element for AC-3.4
    collection.remove_at(0)  # Removes 10
    assert collection.size() == 0  # AC-3.5
    assert collection.head is None  # AC-3.5

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.remove_at(0)  # Removes 10
    assert collection.size() == 0  # AC-3.5
    assert collection.head is None  # AC-3.5

def test_remove_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.remove_at(1)  # AC-3.6
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.remove_at(-1)  # AC-3.6
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        empty_collection.remove_at(0)  # AC-3.6 on empty collection

def test_insert_at_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(30)
    collection.insert_at(1, 20)  # Insert 20 at position 1
    assert collection.head.value == 10  # Verify head value for AC-4.1
    assert collection.head.next.value == 20  # Verify insertion for AC-4.2
    assert collection.head.next.next.value == 30  # Verify next value for AC-4.2
    assert collection.size() == 3  # Verify size for AC-4.2

def test_insert_at_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(20)
    collection.insert_at(0, 10)  # Insert 10 at position 0
    assert collection.head.value == 10  # Check head for AC-4.1
    assert collection.head.next.value == 20  # Check next for AC-4.1
    assert collection.size() == 2  # Verify size for AC-4.1

def test_insert_at_end():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.insert_at(1, 20)  # Insert 20 at position 1
    assert collection.head.value == 10  # Check head for AC-4.3
    assert collection.head.next.value == 20  # Check next for AC-4.3
    assert collection.size() == 2  # Verify size for AC-4.3

def test_insert_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.insert_at(2, 20)  # AC-4.4
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        collection.insert_at(-1, 20)  # AC-4.4
    empty_collection = SinglyLinkedSequence()
    with pytest.raises(Exception, match=r"^index out of bounds$"):
        empty_collection.insert_at(1, 20)  # AC-4.4 on empty collection

def test_membership_search():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.contains(20) == True  # AC-5.1
    assert collection.contains(40) == False  # AC-5.1

def test_search_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(10)
    assert collection.index_of(10) == 0  # AC-5.2 (first occurrence)
    assert collection.index_of(20) == 1  # AC-5.2 (first occurrence)
    assert collection.index_of(40) == -1  # AC-5.3

def test_reverse():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    collection.reverse()
    assert collection.head.value == 30  # Check head for AC-6.1
    assert collection.head.next.value == 20  # Check second for AC-6.1
    assert collection.head.next.next.value == 10  # Check last for AC-6.1
    assert collection.size() == 3  # AC-6.1

def test_reverse_empty_collection():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.size() == 0  # AC-6.2
    assert collection.head is None  # AC-6.2

def test_reverse_single_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.reverse()
    assert collection.head.value == 10  # AC-6.2
    assert collection.size() == 1  # AC-6.2