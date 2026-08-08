def fibonacci_lookup(n):
    if n < 1:
        raise TypeError("Fibonacci numbers start from 1")
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return a