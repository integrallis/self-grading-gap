# file: addition_triangulation/addition.py

from candidate.impl import TwoNumberAdder

class Addition:
    """Adapter for the TwoNumberAdder class."""

    def __init__(self):
        """Initializes the Addition instance."""
        pass

    @staticmethod
    def of(a, b):
        """Adds two numbers using the TwoNumberAdder."""
        return TwoNumberAdder.add(a, b)
