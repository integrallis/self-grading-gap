import pytest

class Calculator:
    def __init__(self):
        self._display = "0"

    def press_digit(self, digit):
        if digit == '0' and self._display == "0":
            return
        if self._display == "0":
            self._display = digit
        else:
            self._display += digit

    def display(self):
        return self._display

class DigitKeyGenerator:
    import random

    def get_digit_key(self, excluded=None):
        if excluded is not None and not isinstance(excluded, str):
            raise NotImplementedError(f"other_than not implemented for {type(excluded)}")
        while True:
            key = str(self.random.randint(0, 9))
            if key != excluded:
                return key
