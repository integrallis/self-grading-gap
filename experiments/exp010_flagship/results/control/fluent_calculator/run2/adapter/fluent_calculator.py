# file: fluent_calculator.py
from candidate import Calculator as _Calculator


class Calculator(_Calculator):
    plus = _Calculator.add
    minus = _Calculator.subtract
