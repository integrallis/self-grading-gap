# candidate/impl.py

class TwoNumberAdder:
    """A simple adder class to sum two integers."""
    
    @staticmethod
    def add_numbers(num1: int, num2: int) -> int:
        """Returns the sum of two whole numbers."""
        return num1 + num2

# Example usage:
if __name__ == "__main__":
    adder = TwoNumberAdder()
    print(adder.add_numbers(3, 5))  # Output: 8
    print(adder.add_numbers(4, 7))  # Output: 11
