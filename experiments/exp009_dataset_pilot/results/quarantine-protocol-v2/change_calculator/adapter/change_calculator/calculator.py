# file: change_calculator/calculator.py

from candidate.impl import CoinChangeMaker

class ChangeCalculator:
    def __init__(self):
        self._coin_change_maker = CoinChangeMaker()

    def calculate_change(self, amount):
        return self._coin_change_maker.make_change(amount)
