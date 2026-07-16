# file: calculator_tdd_ebook/calculator.py
from candidate import Calculator as CandidateCalculator


class Calculator(CandidateCalculator):
    def enter(self, digit):
        return self.press(digit)
