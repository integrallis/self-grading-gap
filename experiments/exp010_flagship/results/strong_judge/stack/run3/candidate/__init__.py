class StackFullError(Exception):
    pass

class StackEmptyError(Exception):
    pass

class BoundedStack:
    def __init__(self, capacity=0):
        if capacity < 0:
            raise Exception("Capacity cannot be negative")
        self.capacity = capacity
        self.stack = []

    def push(self, value):
        if len(self.stack) >= self.capacity:
            raise StackFullError("Stack is full")
        self.stack.append(value)

    def pop(self):
        if self.is_empty():
            raise StackEmptyError("Cannot pop from empty stack")
        return self.stack.pop()

    def is_empty(self):
        return len(self.stack) == 0