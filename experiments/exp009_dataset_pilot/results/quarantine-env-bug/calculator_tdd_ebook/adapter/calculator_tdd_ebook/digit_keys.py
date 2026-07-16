# file: calculator_tdd_ebook/digit_keys.py

from candidate.impl import DigitGenerator as CandidateDigitGenerator

class DigitKeys:
    def __init__(self, exclude_digit=None):
        self._digit_generator = CandidateDigitGenerator(exclude_digit)

    def get_digit(self):
        return self._digit_generator.get_digit()
