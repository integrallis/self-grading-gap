import builtins, pytest; builtins.pytest = pytest

def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {1: 0, 2: 1}
    def fib_helper(n):
        if n in memo:
            return memo[n]
        memo[n] = fib_helper(n - 1) + fib_helper(n - 2)
        return memo[n]
    return fib_helper(n)