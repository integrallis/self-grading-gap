class ChainableCalculator:
    def __init__(self, value=None):
        self._initial_value = value if isinstance(value, int) else None
        self._current_value = self._initial_value if self._initial_value is not None else 0
        self._history = []
        self._redo_stack = []
        self._sealed = False

    def seed(self, value):
        if self._initial_value is None and isinstance(value, int):
            self._initial_value = value
            self._current_value = value
        return self

    def add(self, value):
        if self._sealed or not isinstance(value, int):
            return self
        self._history.append(self._current_value)
        self._current_value += value
        self._redo_stack.clear()
        return self

    def subtract(self, value):
        if self._sealed or not isinstance(value, int):
            return self
        self._history.append(self._current_value)
        self._current_value -= value
        self._redo_stack.clear()
        return self

    def undo(self):
        if self._sealed or not self._history:
            return self
        self._redo_stack.append(self._current_value)
        self._current_value = self._history.pop()
        return self

    def redo(self):
        if self._sealed or not self._redo_stack:
            return self
        self._history.append(self._current_value)
        self._current_value = self._redo_stack.pop()
        return self

    def save(self):
        self._sealed = True
        self._history.clear()
        self._redo_stack.clear()
        return self

    def result(self):
        return self._current_value if self._initial_value is not None else 0


def create_calculator(value=None):
    return ChainableCalculator(value)
