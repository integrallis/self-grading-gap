class BoundedStack:
    def __init__(self, capacity=10):
        if capacity < 0:
            raise Exception("Capacity cannot be negative")
        self.capacity = capacity
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, value):
        if len(self.stack) >= self.capacity:
            raise Exception("Stack is full")
        self.stack.append(value)

    def pop(self):
        if self.is_empty():
            raise Exception("Cannot pop from empty stack")
        return self.stack.pop()