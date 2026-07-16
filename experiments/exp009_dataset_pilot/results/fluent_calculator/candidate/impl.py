class ChainableCalculator:
    def __init__(self):
        self.value = 0
        self.seeded = False
        self.history = []
        self.redo_stack = []
        self.saved = False

    def seed(self, value):
        if not self.seeded and isinstance(value, int):
            self.value = value
            self.seeded = True
            self.history.append(('seed', value))
        return self

    def add(self, value):
        if self.seeded and isinstance(value, int):
            self.value += value
            self.history.append(('add', value))
            self.redo_stack.clear()
        return self

    def subtract(self, value):
        if self.seeded and isinstance(value, int):
            self.value -= value
            self.history.append(('subtract', value))
            self.redo_stack.clear()
        return self

    def result(self):
        return self.value if self.seeded else 0

    def undo(self):
        if self.history and not self.saved:
            last_action = self.history.pop()
            if last_action[0] == 'add':
                self.value -= last_action[1]
                self.redo_stack.append(last_action)
            elif last_action[0] == 'subtract':
                self.value += last_action[1]
                self.redo_stack.append(last_action)
        return self

    def redo(self):
        if self.redo_stack and not self.saved:
            last_action = self.redo_stack.pop()
            if last_action[0] == 'add':
                self.value += last_action[1]
                self.history.append(last_action)
            elif last_action[0] == 'subtract':
                self.value -= last_action[1]
                self.history.append(last_action)
        return self

    def save(self):
        self.saved = True
        self.redo_stack.clear()
        return self

# Example usage:
# calculator = ChainableCalculator()
# result = calculator.seed(10).add(5).subtract(2).undo().result()  # result would be 13
