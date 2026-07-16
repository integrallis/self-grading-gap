from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1
    assert str(collection) == "[]"  # AC-1.1
    assert collection.head is None  # AC-1.1

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    assert collection.size() == 1  # AC-1.2
    assert str(collection) == "[1]"  # AC-1.2

def test_add_successive_elements():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert str(collection) == "[1, 2, 3]"  # AC-1.3

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_end(2)
    collection.add_end(3)
    collection.add_front(1)
    assert str(collection) == "[1, 2, 3]"  # AC-1.4

def test_head_exposes_cells():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.head.value == 1  # AC-1.5
    assert collection.head.next.value == 2  # AC-1.5
    assert collection.head.next.next.value == 3  # AC-1.5
    assert collection.head.next.next.next is None  # AC-1.5

def test_size_tracks_additions_and_removals():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.6
    collection.add_end(1)
    assert collection.size() == 1  # AC-1.6
    collection.add_end(2)
    assert collection.size() == 2  # AC-1.6
    collection.remove(0)
    assert collection.size() == 1  # AC-1.6
    collection.remove(0)
    assert collection.size() == 0  # AC-1.6

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.read(0) == 1  # AC-2.1
    assert collection.read(1) == 2  # AC-2.1
    assert collection.read(2) == 3  # AC-2.1

def test_read_out_of_range():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    try:
        collection.read(3)  # AC-2.2
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-2.2

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.remove(1) == 2  # AC-3.1
    assert str(collection) == "[1, 3]"  # AC-3.1

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.remove(0)
    assert str(collection) == "[2]"  # AC-3.2

def test_remove_middle_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    collection.remove(1)
    assert str(collection) == "[1, 3]"  # AC-3.3

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.remove(1)
    assert str(collection) == "[1]"  # AC-3.4

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.remove(0)
    assert collection.size() == 0  # AC-3.5
    assert collection.head is None  # AC-3.5

def test_remove_out_of_range():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    try:
        collection.remove(1)  # AC-3.6
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-3.6

def test_insert_at_position_zero():
    collection = SinglyLinkedSequence()
    collection.add_end(2)
    collection.insert(0, 1)
    assert str(collection) == "[1, 2]"  # AC-4.1

def test_insert_at_middle_position():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(3)
    collection.insert(1, 2)
    assert str(collection) == "[1, 2, 3]"  # AC-4.2

def test_insert_at_end():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.insert(1, 2)
    assert str(collection) == "[1, 2]"  # AC-4.3

def test_insert_out_of_range():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    try:
        collection.insert(2, 2)  # AC-4.4
    except IndexError as e:
        assert str(e) == "index out of bounds"  # AC-4.4

def test_membership_check():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    assert collection.contains(1) is True  # AC-5.1
    assert collection.contains(3) is False  # AC-5.1

def test_position_of_value():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    assert collection.index(2) == 1  # AC-5.2
    assert collection.index(4) == -1  # AC-5.3

def test_reverse_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(1)
    collection.add_end(2)
    collection.add_end(3)
    collection.reverse()
    assert str(collection) == "[3, 2, 1]"  # AC-6.1

def test_reverse_empty_or_single_element():
    empty_collection = SinglyLinkedSequence()
    empty_collection.reverse()
    assert str(empty_collection) == "[]"  # AC-6.2

    single_element_collection = SinglyLinkedSequence()
    single_element_collection.add_end(1)
    single_element_collection.reverse()
    assert str(single_element_collection) == "[1]"  # AC-6.2