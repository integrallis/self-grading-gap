from solution import SinglyLinkedSequence

def test_empty_collection():
    collection = SinglyLinkedSequence()
    assert collection.size() == 0  # AC-1.1: size is zero
    assert collection.head is None  # AC-1.1: no head cell
    assert collection.contents() == []  # AC-1.1: contents is an empty sequence

def test_add_to_empty_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    assert collection.size() == 1  # AC-1.2: size is now one
    assert collection.contents() == [10]  # AC-1.2: contents is [10]

def test_successive_additions():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.add_end(30)
    assert collection.contents() == [10, 20, 30]  # AC-1.3: preserves insertion order

def test_add_to_front():
    collection = SinglyLinkedSequence()
    collection.add_end(20)
    collection.add_end(30)
    collection.add_front(10)
    assert collection.contents() == [10, 20, 30]  # AC-1.4: adds 10 at the front

def test_head_exposes_chain():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.add_end(30)
    head = collection.head
    assert head.value == 10  # AC-1.5: head cell value is 10
    assert head.next.value == 20  # AC-1.5: next cell value is 20
    assert head.next.next.value == 30  # AC-1.5: final cell value is 30
    assert head.next.next.next is None  # AC-1.5: final cell links to nothing

def test_size_tracking():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.remove(0)  # Removes 10
    assert collection.size() == 1  # AC-1.6: size is 1 after removal
    collection.add_front(30)
    assert collection.size() == 2  # AC-1.6: size is 2 after addition

def test_read_position():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.add_end(30)
    assert collection.read(0) == 10  # AC-2.1: reads first element
    assert collection.read(1) == 20  # AC-2.1: reads second element
    assert collection.read(2) == 30  # AC-2.1: reads last element

def test_read_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    try:
        collection.read(3)  # AC-2.2: out of bounds
    except IndexError as e:
        assert str(e) == "index out of bounds"

def test_remove_element():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.add_end(30)
    assert collection.remove(1) == 20  # AC-3.1: removes 20 and returns it
    assert collection.contents() == [10, 30]  # AC-3.3: links 10 directly to 30

def test_remove_first_element():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    assert collection.remove(0) == 10  # AC-3.1: removes first element
    assert collection.head.value == 20  # AC-3.2: head is now 20

def test_remove_last_element():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    assert collection.remove(1) == 20  # AC-3.1: removes last element
    assert collection.contents() == [10]  # AC-3.4: remaining element is 10

def test_remove_only_element():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    assert collection.remove(0) == 10  # AC-3.1: removes the only element
    assert collection.size() == 0  # AC-3.5: collection is now empty
    assert collection.head is None  # AC-3.5: no head cell

def test_remove_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    try:
        collection.remove(1)  # AC-3.6: out of bounds
    except IndexError as e:
        assert str(e) == "index out of bounds"

def test_insert_at_position_zero():
    collection = SinglyLinkedSequence()
    collection.add_end(20)
    collection.insert(0, 10)  # AC-4.1: inserts at position 0
    assert collection.contents() == [10, 20]  # Collection is [10, 20]

def test_insert_middle_position():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(30)
    collection.insert(1, 20)  # AC-4.2: inserts 20 at position 1
    assert collection.contents() == [10, 20, 30]  # Collection is [10, 20, 30]

def test_insert_at_end():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.insert(1, 20)  # Insert 20 at position 1
    collection.insert(2, 30)  # AC-4.3: appends 30 at end
    assert collection.contents() == [10, 20, 30]  # Collection is [10, 20, 30]

def test_insert_out_of_bounds():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    try:
        collection.insert(2, 20)  # AC-4.4: out of bounds
    except IndexError as e:
        assert str(e) == "index out of bounds"

def test_value_membership():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    assert collection.contains(10) is True  # AC-5.1: 10 is present
    assert collection.contains(30) is False  # AC-5.1: 30 is absent

def test_value_position():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    assert collection.position(20) == 1  # AC-5.2: first occurrence of 20 is at index 1
    assert collection.position(30) == -1  # AC-5.3: absent value returns -1

def test_reverse_collection():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.add_end(20)
    collection.add_end(30)
    collection.reverse()
    assert collection.contents() == [30, 20, 10]  # AC-6.1: reversed order

def test_reverse_empty_collection():
    collection = SinglyLinkedSequence()
    collection.reverse()
    assert collection.contents() == []  # AC-6.2: empty remains unchanged

def test_reverse_single_element():
    collection = SinglyLinkedSequence()
    collection.add_end(10)
    collection.reverse()
    assert collection.contents() == [10]  # AC-6.2: single remains unchanged