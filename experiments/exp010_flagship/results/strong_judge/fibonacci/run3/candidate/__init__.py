import builtins, pytest; builtins.pytest = pytest

def fibonacci_lookup(n):
    if n <= 0:
        raise TypeError("Fibonacci numbers start from 1")
    a, b = 0, 1
    for _ in range(1, n):
        a, b = b, a + b
    return a