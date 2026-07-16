# candidate/impl.py

class BracketValidator:
    @staticmethod
    def is_balanced(bracket_string: str) -> bool:
        balance = 0
        for char in bracket_string:
            if char == '[':
                balance += 1
            elif char == ']':
                balance -= 1
            
            # If at any point balance is negative, we have a closing bracket without a matching opener
            if balance < 0:
                return False
        
        # In the end, balance should be zero for the brackets to be balanced
        return balance == 0

# Example usage:
if __name__ == "__main__":
    validator = BracketValidator()
    test_cases = [
        "",          # balanced
        "[]",       # balanced
        "[][]",     # balanced
        "[[]]",     # balanced
        "[[[][]]]", # balanced
        "][" ,      # unbalanced
        "][][",     # unbalanced
        "[",        # unbalanced
        "[]]",      # unbalanced
        "[[",       # unbalanced
        "[]]",      # unbalanced
        "[][]][",   # unbalanced
        "]]",       # unbalanced
        "[[[]",     # unbalanced
        "[" * 50 + "]" * 50 # balanced
    ]
    
    for case in test_cases:
        result = validator.is_balanced(case)
        print(f"'{case}': {'Balanced' if result else 'Unbalanced'}")
