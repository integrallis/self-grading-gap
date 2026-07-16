# file: code_breaker.py
from candidate import score_guess, validate_guess, validate_secret


class CodeBreaker:
    def __init__(self, secret, guess=None):
        self.secret = secret
        self.initial_guess = guess

    def guess(self, guess):
        return score_guess(self.secret, guess)

    def raises(self, secret, guess=None):
        return validate_guess(secret, guess)
