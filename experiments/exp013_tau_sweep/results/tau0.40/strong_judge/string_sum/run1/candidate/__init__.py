'''The solution package.'''

__version__ = "0.1.0"

def add_text_numbers(num1: str, num2: str) -> str:
    # Convert the numeric texts to integers, treating empty strings as 0
    sum_result = int(num1 or '0') + int(num2 or '0')
    return str(sum_result)