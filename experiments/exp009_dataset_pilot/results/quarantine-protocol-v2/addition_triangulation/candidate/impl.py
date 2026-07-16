# candidate/impl.py

class TwoNumberAdder:
    """A simple adder class to sum two integers."""

    @staticmethod
    def add(a: int, b: int) -> int:
        """
        Returns the sum of two integers.

        :param a: First integer.
        :param b: Second integer.
        :return: The sum of a and b.
        """
        return a + b

# Example usage:
if __name__ == "__main__":
    adder = TwoNumberAdder()
    print(adder.add(3, 5))  # Output: 8
    print(adder.add(4, 7))  # Output: 11
