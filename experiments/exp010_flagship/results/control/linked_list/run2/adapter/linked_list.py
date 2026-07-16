# file: linked_list.py
from candidate import SinglyLinkedSequence


class LinkedList(SinglyLinkedSequence):
    append = SinglyLinkedSequence.add_end
    prepend = SinglyLinkedSequence.add_front
    get = SinglyLinkedSequence.read
    insert_at = SinglyLinkedSequence.insert
    index_of = SinglyLinkedSequence.index

    def to_list(self):
        return list(map(self.read, range(self.size())))
