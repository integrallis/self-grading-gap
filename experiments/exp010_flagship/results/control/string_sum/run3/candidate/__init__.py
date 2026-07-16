def add_text_numbers(num1: str, num2: str) -> str:
    # Strip leading/trailing spaces and convert to integers
    n1 = int(num1.strip() or '0')
    n2 = int(num2.strip() or '0')
    # Return the sum as a string
    return str(n1 + n2)