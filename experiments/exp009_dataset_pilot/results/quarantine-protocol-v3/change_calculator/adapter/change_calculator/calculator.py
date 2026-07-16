# file: change_calculator/calculator.py
from candidate.impl import CoinChangeMaker


class ChangeCalculator(CoinChangeMaker):
    calculate_change = CoinChangeMaker.make_change
