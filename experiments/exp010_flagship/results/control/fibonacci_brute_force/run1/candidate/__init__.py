def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)