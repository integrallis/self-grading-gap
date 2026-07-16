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
            
            # If balance goes negative, there is a closing bracket without a matching opening
            if balance < 0:
                return False
        
        # At the end, balance must be zero for the brackets to be balanced
        return balance == 0

# Usage example (for testing purposes, can be removed in the final module):
if __name__ == "__main__":
    test_cases = [
        "",                # balanced
        "[]",              # balanced
        "[][]",            # balanced
        "[[]]",            # balanced
        "[[[][]]]",        # balanced
        "][" ,             # unbalanced
        "][][",            # unbalanced
        "[",               # unbalanced
        "[]]",             # unbalanced
        "[]][",            # unbalanced
        "[[",              # unbalanced
        "[]][",           # unbalanced
        "[]]",             # unbalanced
        "[[[]",            # unbalanced
        "[" * 50 + "]" * 50  # balanced
    ]

    for case in test_cases:
        print(f"'{case}': {BracketValidator.is_balanced(case)}")
