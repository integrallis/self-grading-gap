# candidate/impl.py

class ChainableCalculator:
    def __init__(self):
        self._value = 0
        self._history = []
        self._redo_stack = []
        self._is_saved = False
        self._is_seeded = False

    def seed(self, value):
        if not self._is_seeded and isinstance(value, int):
            self._value = value
            self._is_seeded = True
            self._history.append(('seed', value))
            self._redo_stack.clear()
        return self

    def add(self, value):
        if self._is_saved or not self._is_seeded or not isinstance(value, int):
            return self
        self._value += value
        self._history.append(('add', value))
        self._redo_stack.clear()
        return self

    def subtract(self, value):
        if self._is_saved or not self._is_seeded or not isinstance(value, int):
            return self
        self._value -= value
        self._history.append(('subtract', value))
        self._redo_stack.clear()
        return self

    def undo(self):
        if not self._is_seeded or not self._history:
            return self
        action, value = self._history.pop()
        if action == 'add':
            self._value -= value
            self._redo_stack.append(('add', value))
        elif action == 'subtract':
            self._value += value
            self._redo_stack.append(('subtract', value))
        return self

    def redo(self):
        if not self._is_seeded or not self._redo_stack or self._is_saved:
            return self
        action, value = self._redo_stack.pop()
        if action == 'add':
            self._value += value
            self._history.append(('add', value))
        elif action == 'subtract':
            self._value -= value
            self._history.append(('subtract', value))
        return self

    def save(self):
        self._is_saved = True
        self._redo_stack.clear()
        return self

    def result(self):
        return self._value if self._is_seeded else 0
