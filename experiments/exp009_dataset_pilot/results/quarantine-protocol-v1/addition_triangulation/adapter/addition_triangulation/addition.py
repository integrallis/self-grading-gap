# file: addition_triangulation/addition.py

from candidate.impl import TwoNumberAdder

class Addition:
    """Adapter class to expose the add_numbers method."""

    @staticmethod
    def add(num1, num2):
        """
        Adds two numbers using the TwoNumberAdder implementation.

        Parameters:
        num1: The first number.
        num2: The second number.

        Returns:
        The sum of num1 and num2.
        """
        return TwoNumberAdder.add_numbers(num1, num2)
