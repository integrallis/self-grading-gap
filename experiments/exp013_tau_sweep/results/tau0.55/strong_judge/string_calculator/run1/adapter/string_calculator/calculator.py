# file: string_calculator/calculator.py
from candidate import add_numbers as _add_numbers


class Calculator:
    add = staticmethod(_add_numbers)
    raises = staticmethod(_add_numbers)
