# file: change_calculator/calculator.py
from candidate import make_change as _make_change


class ChangeCalculator:
    def calculate_change(self, amount):
        return _make_change(amount)
