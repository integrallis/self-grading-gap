class ChainableCalculator:
    def __init__(self):
        self.value = 0
        self.seeded = False
        self.history = []
        self.redo_stack = []
    
    def seed(self, value):
        if isinstance(value, int):
            if not self.seeded:
                self.value = value
                self.seeded = True
        return self

    def add(self, value):
        if self.seeded and isinstance(value, int):
            self.history.append(self.value)
            self.value += value
            self.redo_stack.clear()
        return self

    def subtract(self, value):
        if self.seeded and isinstance(value, int):
            self.history.append(self.value)
            self.value -= value
            self.redo_stack.clear()
        return self

    def result(self):
        return self.value if self.seeded else 0

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
        self.history.clear()
        self.redo_stack.clear()
        return self


# Example usage:
# calculator = ChainableCalculator()
# result = calculator.seed(10).add(5).subtract(2).undo().result()  # Should return 13
