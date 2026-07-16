# candidate/impl.py

class TwoNumberAdder:
    """A simple class to add two whole numbers."""
    
    @staticmethod
    def add_numbers(num1: int, num2: int) -> int:
        """Returns the sum of two integers.
        
        Args:
            num1 (int): The first integer to add.
            num2 (int): The second integer to add.
        
        Returns:
            int: The sum of num1 and num2.
        
        Example:
            >>> TwoNumberAdder.add_numbers(3, 5)
            8
        """
        return num1 + num2
