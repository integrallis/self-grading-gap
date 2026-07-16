from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1: size is zero
    assert str(collection) == "[]"  # AC-1.1: contents are empty
    assert collection.head is None  # AC-1.1: no head cell

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    assert collection.size() == 1  # AC-1.2: size is now one
    assert str(collection) == "[10]"  # AC-1.2: contents are [10]

def test_successive_additions():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert str(collection) == "[10, 20, 30]"  # AC-1.3: preserves insertion order

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_to_end(20)
    collection.add_to_front(10)
    assert str(collection) == "[10, 20]"  # AC-1.4: added at the front

def test_head_exposes_cells():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    assert collection.head.value == 10  # AC-1.5: head value is 10
    assert collection.head.next.value == 20  # AC-1.5: next cell value is 20
    assert collection.head.next.next.value == 30  # AC-1.5: next next cell value is 30
    assert collection.head.next.next.next is None  # AC-1.5: last cell links to nothing

def test_size_tracking():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    assert collection.size() == 2  # AC-1.6: size is 2
    collection.remove(0)
    assert collection.size() == 1  # AC-1.6: size is 1
    collection.add_to_front(30)
    assert collection.size() == 2  # AC-1.6: size is 2 again

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    assert collection.read(0) == 10  # AC-2.1: position 0 is 10
    assert collection.read(1) == 20  # AC-2.1: position 1 is 20

def test_read_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    try:
        collection.read(2)  # AC-2.2: position out of range
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-2.2: error message

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    removed_value = collection.remove(0)
    assert removed_value == 10  # AC-3.1: removed value is 10
    assert str(collection) == "[20]"  # AC-3.2: head now is 20

def test_remove_middle_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(30)
    removed_value = collection.remove(1)
    assert removed_value == 20  # AC-3.1: removed value is 20
    assert str(collection) == "[10, 30]"  # AC-3.3: links are correct

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    removed_value = collection.remove(1)
    assert removed_value == 20  # AC-3.1: removed value is 20
    assert str(collection) == "[10]"  # AC-3.4: last element removed

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    removed_value = collection.remove(0)
    assert removed_value == 10  # AC-3.1: removed value is 10
    assert collection.size() == 0  # AC-3.5: collection is empty
    assert collection.head is None  # AC-3.5: no head

def test_remove_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    try:
        collection.remove(1)  # AC-3.6: position out of range
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-3.6: error message

def test_insert_at_position_zero():
    collection = SinglyLinkedSequence()
    collection.add_to_end(20)
    collection.insert(0, 10)
    assert str(collection) == "[10, 20]"  # AC-4.1: inserting at position 0

def test_insert_middle_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(30)
    collection.insert(1, 20)
    assert str(collection) == "[10, 20, 30]"  # AC-4.2: inserting in the middle

def test_insert_at_end_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.insert(1, 20)
    collection.insert(2, 30)
    assert str(collection) == "[10, 20, 30]"  # AC-4.3: inserting at the end

def test_insert_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    try:
        collection.insert(2, 20)  # AC-4.4: position out of range
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-4.4: error message

def test_membership_check():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    assert collection.contains(10) is True  # AC-5.1: membership returns true for stored value
    assert collection.contains(20) is False  # AC-5.1: membership returns false for absent value

def test_first_occurrence_position():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.add_to_end(10)
    assert collection.index_of(10) == 0  # AC-5.2: first occurrence is at position 0
    assert collection.index_of(20) == 1  # AC-5.2: first occurrence is at position 1
    assert collection.index_of(30) == -1  # AC-5.3: absent value returns -1

def test_reverse_collection():
    collection = SinglyLinkedSequence()
    collection.add_to_end(10)
    collection.add_to_end(20)
    collection.reverse()
    assert str(collection) == "[20, 10]"  # AC-6.1: order is reversed

def test_reverse_empty_or_single_element():
    collection_empty = SinglyLinkedSequence()
    collection_empty.reverse()
    assert str(collection_empty) == "[]"  # AC-6.2: empty collection unchanged

    collection_single = SinglyLinkedSequence()
    collection_single.add_to_end(10)
    collection_single.reverse()
    assert str(collection_single) == "[10]"  # AC-6.2: single element unchanged