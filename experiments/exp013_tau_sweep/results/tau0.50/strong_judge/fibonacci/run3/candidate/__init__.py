def fibonacci_number_at_position(n):
    if n < 1:
        raise TypeError("Fibonacci numbers start from 1")
    elif n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n):
            a, b = b, a + b
        return b