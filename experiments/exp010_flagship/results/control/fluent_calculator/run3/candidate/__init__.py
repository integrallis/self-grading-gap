class Calculator:
    def __init__(self):
        self.value = 0
        self.history = []
        self.redo_stack = []
        self.saved = False

    def seed(self, value):
        if not self.history and self.value == 0:
            self.value = value
        return self

    def add(self, value):
        if isinstance(value, (int, float)):
            if self.saved:
                self.history.clear()
                self.saved = False
            self.history.append(('add', value))
            self.value += value
            self.redo_stack.clear()  # Clear redo stack on new operation
        return self

    def subtract(self, value):
        if isinstance(value, (int, float)):
            if self.saved:
                self.history.clear()
                self.saved = False
            self.history.append(('subtract', value))
            self.value -= value
            self.redo_stack.clear()  # Clear redo stack on new operation
        return self

    def result(self):
        return self.value

    def undo(self):
        if self.history and not self.saved:
            operation, value = self.history.pop()
            if operation == 'add':
                self.value -= value
            elif operation == 'subtract':
                self.value += value
            self.redo_stack.append((operation, value))

    def redo(self):
        if self.redo_stack:
            operation, value = self.redo_stack.pop()
            if operation == 'add':
                self.value += value
            elif operation == 'subtract':
                self.value -= value
            self.history.append((operation, value))

    def save(self):
        self.saved = True

    def reset(self):
        self.value = 0
        self.history.clear()
        self.redo_stack.clear()
        self.saved = False
