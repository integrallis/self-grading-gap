def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {}
    def fib(n):
        if n in memo:
            return memo[n]
        if n == 1:
            return 0
        elif n == 2:
            return 1
        else:
            memo[n] = fib(n - 1) + fib(n - 2)
            return memo[n]
    return fib(n)