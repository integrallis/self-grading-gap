# file: addition_triangulation/addition.py

from candidate.impl import TwoNumberAdder

class Addition:
    """Adapter class to expose the addition functionality."""
    
    @staticmethod
    def add(num1, num2):
        """Adds two numbers using the TwoNumberAdder implementation.
        
        Args:
            num1: The first number to add.
            num2: The second number to add.
        
        Returns:
            The sum of num1 and num2.
            
        Example:
            >>> Addition.add(3, 5)
            8
        """
        return TwoNumberAdder.add_numbers(num1, num2)
