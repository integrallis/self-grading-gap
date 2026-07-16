# file: calculator_tdd_ebook/digit_keys.py
from candidate import DigitKeyGenerator as _CandidateDigitKeyGenerator


class DigitKeys(_CandidateDigitKeyGenerator):
    other_than = _CandidateDigitKeyGenerator.get_digit_key
