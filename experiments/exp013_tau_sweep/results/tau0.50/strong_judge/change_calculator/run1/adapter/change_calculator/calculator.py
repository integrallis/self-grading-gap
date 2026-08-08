# file: change_calculator/calculator.py
from candidate import make_change


class ChangeCalculator:
    def calculate_change(self, amount):
        return make_change(amount)
