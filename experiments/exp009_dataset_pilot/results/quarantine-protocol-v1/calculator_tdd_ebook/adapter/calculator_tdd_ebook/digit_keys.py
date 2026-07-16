# file: calculator_tdd_ebook/digit_keys.py

from candidate.impl import Calculator as _Calculator

class DigitKeys:
    def __init__(self):
        self._calculator = _Calculator()

    def press(self, digit):
        self._calculator.press_digit(digit)

    def display(self):
        return self._calculator.get_display()
