def fibonacci_lookup(position):
    if position <= 0:
        raise TypeError("Fibonacci numbers start from 1")
    a, b = 0, 1
    for _ in range(1, position):
        a, b = b, a + b
    return a