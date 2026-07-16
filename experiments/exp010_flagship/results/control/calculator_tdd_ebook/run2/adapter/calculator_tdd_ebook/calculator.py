# file: calculator_tdd_ebook/calculator.py
from candidate import Calculator as _Calculator


class Calculator(_Calculator):
    def enter(self, digit):
        return self.press(digit)
