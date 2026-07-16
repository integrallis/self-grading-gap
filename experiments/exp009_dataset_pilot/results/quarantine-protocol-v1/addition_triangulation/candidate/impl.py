# candidate/impl.py

class TwoNumberAdder:
    """A simple adder class that sums two integers."""

    @staticmethod
    def add_numbers(num1: int, num2: int) -> int:
        """
        Returns the sum of two integers.

        Parameters:
        num1 (int): The first integer.
        num2 (int): The second integer.

        Returns:
        int: The sum of num1 and num2.
        """
        return num1 + num2

# The following code can be used for testing the functionality
if __name__ == "__main__":
    # Example of adding two numbers
    result1 = TwoNumberAdder.add_numbers(3, 5)
    print(f"Adding 3 and 5 yields: {result1}")  # Expected output: 8

    result2 = TwoNumberAdder.add_numbers(4, 7)
    print(f"Adding 4 and 7 yields: {result2}")  # Expected output: 11
