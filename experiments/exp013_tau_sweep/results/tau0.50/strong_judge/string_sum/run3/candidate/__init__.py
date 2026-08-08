def add_text_numbers(num1: str, num2: str) -> str:
    # Convert the inputs to integers, treating empty strings as 0
    return str(int(num1 or '0') + int(num2 or '0'))