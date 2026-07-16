# file: code_breaker.py
from candidate import score_guess, validate_guess


class CodeBreaker:
    def __init__(self, secret, expected=None):
        self.secret = secret
        self.expected = expected

    def guess(self, guess):
        return score_guess(self.secret, guess)

    def raises(self, guess, expected=None):
        return validate_guess(self.secret, guess)
