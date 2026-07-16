# file: calculator_tdd_ebook/calculator.py

from candidate.impl import Calculator as _Calculator

class Calculator:
    def __init__(self):
        self._calculator = _Calculator()

    def press_digit(self, digit):
        self._calculator.press_digit(digit)

    def get_display(self):
        return self._calculator.get_display()
