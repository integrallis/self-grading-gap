class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class SinglyLinkedSequence:
    def __init__(self):
        self.head = None
        self._size = 0

    def add_to_end(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self._size += 1

    def add_to_front(self, value):
        new_node = Node(value)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def size(self):
        return self._size

    def __str__(self):
        values = []
        current = self.head
        while current:
            values.append(current.value)
            current = current.next
        return f"[{', '.join(map(str, values))}]"

    def read(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of bounds")
        current = self.head
        for _ in range(index):
            current = current.next
        return current.value

    def remove(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("index out of bounds")
        if index == 0:
            removed_value = self.head.value
            self.head = self.head.next
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            removed_value = current.next.value
            current.next = current.next.next
        self._size -= 1
        return removed_value

    def insert(self, index, value):
        if index < 0 or index > self._size:
            raise IndexError("index out of bounds")
        if index == 0:
            self.add_to_front(value)
            return
        new_node = Node(value)
        current = self.head
        for _ in range(index - 1):
            current = current.next
        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def contains(self, value):
        current = self.head
        while current:
            if current.value == value:
                return True
            current = current.next
        return False

    def index_of(self, value):
        current = self.head
        index = 0
        while current:
            if current.value == value:
                return index
            current = current.next
            index += 1
        return -1

    def reverse(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
