# file: prime_factor/prime_factor.py
from candidate import prime_factors as _generate


class PrimeFactor:
    generate = staticmethod(_generate)
