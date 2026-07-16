def is_balanced(s):
    depth = 0
    for char in s:
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
        if depth < 0:
            return False
    return depth == 0
