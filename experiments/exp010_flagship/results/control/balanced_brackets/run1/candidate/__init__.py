def is_balanced(s):
    balance = 0
    for char in s:
        if char == '[':
            balance += 1
        elif char == ']':
            balance -= 1
        if balance < 0:
            return False
    return balance == 0