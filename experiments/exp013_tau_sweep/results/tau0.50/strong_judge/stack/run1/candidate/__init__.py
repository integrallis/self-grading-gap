class EmptyStackError(Exception):
    pass

class FullStackError(Exception):
    pass

class BoundedStack:
    def __init__(self, max_capacity=10):
        if max_capacity < 0:
            raise Exception("Capacity cannot be negative")
        self.max_capacity = max_capacity
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        if len(self.items) >= self.max_capacity:
            raise FullStackError("Stack is full")
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise EmptyStackError("Cannot pop from empty stack")
        return self.items.pop()