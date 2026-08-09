def is_balanced(text: str) -> bool:
    balance = 0
    for char in text:
        if char == '[':
            balance += 1
        elif char == ']':
            balance -= 1
        if balance < 0:
            return False
    return balance == 0