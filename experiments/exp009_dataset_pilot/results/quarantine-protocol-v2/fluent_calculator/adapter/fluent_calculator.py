# file: fluent_calculator.py

from candidate.impl import create_calculator

class Calculator:
    def __init__(self):
        self._calculator = create_calculator()

    def seed(self, value):
        return self._calculator.seed(value)

    def plus(self, value):
        return self._calculator.add(value)

    def minus(self, value):
        return self._calculator.subtract(value)

    def undo(self):
        return self._calculator.undo()

    def redo(self):
        return self._calculator.redo()

    def save(self):
        return self._calculator.save()

    def result(self):
        return self._calculator.result()
