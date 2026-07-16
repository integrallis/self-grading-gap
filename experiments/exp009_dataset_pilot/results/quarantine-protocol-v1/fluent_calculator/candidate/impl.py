class ChainableCalculator:
    def __init__(self):
        self._value = 0
        self._seeded = False
        self._history = []
        self._undo_stack = []
        self._saved = False

    def seed(self, value):
        if not self._seeded and isinstance(value, int):
            self._value = value
            self._seeded = True
        return self

    def add(self, value):
        if self._saved or not self._seeded or not isinstance(value, int):
            return self
        self._history.append(self._value)
        self._value += value
        self._undo_stack.clear()
        return self

    def subtract(self, value):
        if self._saved or not self._seeded or not isinstance(value, int):
            return self
        self._history.append(self._value)
        self._value -= value
        self._undo_stack.clear()
        return self

    def result(self):
        return self._value if self._seeded else 0

    def undo(self):
        if self._history and not self._saved:
            self._undo_stack.append(self._history.pop())
            self._value = self._history[-1] if self._history else self._value
        return self

    def redo(self):
        if self._undo_stack and not self._saved:
            self._history.append(self._value)
            self._value = self._undo_stack.pop()
        return self

    def save(self):
        self._saved = True
        self._undo_stack.clear()
        return self

def create_calculator():
    return ChainableCalculator()
