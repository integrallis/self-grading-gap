# file: fluent_calculator.py
from candidate.impl import ChainableCalculator


class Calculator(ChainableCalculator):
    plus = ChainableCalculator.add
    minus = ChainableCalculator.subtract
