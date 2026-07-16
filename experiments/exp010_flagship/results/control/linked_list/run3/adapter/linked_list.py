# file: linked_list.py
from candidate import SinglyLinkedSequence


class LinkedList(SinglyLinkedSequence):
    append = SinglyLinkedSequence.add_end
    prepend = SinglyLinkedSequence.add_front
    get = SinglyLinkedSequence.read
    insert_at = SinglyLinkedSequence.insert
    index_of = SinglyLinkedSequence.position
    to_list = SinglyLinkedSequence.contents
