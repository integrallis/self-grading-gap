class Calculator:
    def __init__(self):
        self._value = 0
        self._history = []
        self._redo_stack = []
        self._saved_history = None

    def seed(self, value):
        if isinstance(value, int):
            if not self._history and self._value == 0:
                self._value = value
                self._history = []  # Reset history on valid seed
                self._redo_stack = []
            elif self._value != value:
                return self  # Ignore second seed if it's different
        return self

    def add(self, value):
        if isinstance(value, int):
            if self._history or self._value != 0:
                self._history.append(self._value)
                self._value += value
                self._redo_stack.clear()  # Clear redo stack on new operation
        return self

    def subtract(self, value):
        if isinstance(value, int):
            if self._history or self._value != 0:
                self._history.append(self._value)
                self._value -= value
                self._redo_stack.clear()  # Clear redo stack on new operation
        return self

    def result(self):
        return self._value

    def undo(self):
        if self._history:
            self._redo_stack.append(self._value)
            self._value = self._history.pop()
        return self

    def redo(self):
        if self._redo_stack:
            self._history.append(self._value)
            self._value = self._redo_stack.pop()
        return self

    def save(self):
        self._saved_history = (self._value, self._history.copy())
        self._redo_stack.clear()  # Clear redo stack after save
        return self
