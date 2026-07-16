# file: fluent_calculator.py
from candidate import Calculator as _Calculator


class Calculator(_Calculator):
    def plus(self, value):
        return self.add(value)

    def minus(self, value):
        return self.subtract(value)
