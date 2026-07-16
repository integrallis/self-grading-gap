# candidate/impl.py

class BracketValidator:
    @staticmethod
    def is_balanced(s: str) -> bool:
        balance = 0
        
        for char in s:
            if char == '[':
                balance += 1
            elif char == ']':
                balance -= 1
            
            # If balance goes negative, there are unmatched closing brackets
            if balance < 0:
                return False
        
        # The string is balanced if balance is zero at the end
        return balance == 0

def validate_bracket_string(s: str) -> str:
    if BracketValidator.is_balanced(s):
        return "yes"
    else:
        return "no"
