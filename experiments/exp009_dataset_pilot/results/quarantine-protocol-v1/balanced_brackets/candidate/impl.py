# candidate/impl.py

class BracketValidator:
    @staticmethod
    def is_balanced(s: str) -> bool:
        """
        Check if the provided string of brackets is balanced.
        
        Parameters:
        s (str): The string containing only square brackets to validate.
        
        Returns:
        bool: True if balanced, False otherwise.
        """
        balance = 0
        for char in s:
            if char == '[':
                balance += 1
            elif char == ']':
                balance -= 1
            
            if balance < 0:
                return False
        
        return balance == 0

# Example usage:
# if __name__ == "__main__":
#     print(BracketValidator.is_balanced("[]"))  # Should return True
#     print(BracketValidator.is_balanced("[[[]]]"))  # Should return True
#     print(BracketValidator.is_balanced("]["))  # Should return False
#     print(BracketValidator.is_balanced("[[[]]"))  # Should return False
