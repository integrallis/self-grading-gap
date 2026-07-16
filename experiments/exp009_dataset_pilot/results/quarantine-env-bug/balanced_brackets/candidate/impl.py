# candidate/impl.py

class BracketValidator:
    @staticmethod
    def is_balanced(input_string: str) -> str:
        balance_counter = 0
        
        for char in input_string:
            if char == '[':
                balance_counter += 1
            elif char == ']':
                balance_counter -= 1
            
            if balance_counter < 0:
                return "no"

        return "yes" if balance_counter == 0 else "no"
