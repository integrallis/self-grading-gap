# file: change_calculator/calculator.py
from candidate.impl import CoinChangeMaker as ChangeCalculator

ChangeCalculator.calculate_change = ChangeCalculator.make_change
