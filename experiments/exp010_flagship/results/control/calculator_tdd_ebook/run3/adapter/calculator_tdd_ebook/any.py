# file: calculator_tdd_ebook/any.py
from candidate import DigitGenerator


class Any(DigitGenerator):
    def of(self, value):
        return value

    def other_than(self, value):
        return self.get_digit(value)

    def raises(self, value):
        return value

    def string_consisting_of(self, *values):
        return self.get_digit(*values)
