# file: prime_factor/prime_factor.py
from candidate import prime_factor_decomposition


class PrimeFactor:
    def generate(self, value):
        return prime_factor_decomposition(value)
