class Calculator:
    def __init__(self):
        self.value = 0
        self.history = []
        self.redo_stack = []
        self.seeded = False
        self.saved_value = None

    def seed(self, value):
        if not self.seeded and isinstance(value, int):
            self.value = value
            self.seeded = True
            self.history = []  # Reset history on valid seed
        return self

    def add(self, value):
        if not self.seeded or not isinstance(value, int):
            return self
        self.history.append(self.value)
        self.value += value
        self.redo_stack.clear()  # Clear redo history
        return self

    def subtract(self, value):
        if not self.seeded or not isinstance(value, int):
            return self
        self.history.append(self.value)
        self.value -= value
        self.redo_stack.clear()  # Clear redo history
        return self

    def result(self):
        return self.value

    def undo(self):
        if self.history:
            self.redo_stack.append(self.value)
            self.value = self.history.pop()
        return self

    def redo(self):
        if self.redo_stack:
            self.history.append(self.value)
            self.value = self.redo_stack.pop()
        return self

    def save(self):
        self.saved_value = self.value
        self.history = []  # Clear history on save
        self.redo_stack.clear()  # Clear redo history
        return self
