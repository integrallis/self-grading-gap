# file: linked_list.py
from candidate import SinglyLinkedSequence


class LinkedList(SinglyLinkedSequence):
    append = SinglyLinkedSequence.add_to_end
    prepend = SinglyLinkedSequence.add_to_front
    get = SinglyLinkedSequence.read_at
    remove = SinglyLinkedSequence.remove_at
    to_list = SinglyLinkedSequence.contents
