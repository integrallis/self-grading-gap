# file: addition_triangulation/addition.py
from candidate.impl import TwoNumberAdder


class Addition:
    @staticmethod
    def of(num1, num2):
        return TwoNumberAdder.add_numbers(num1, num2)
