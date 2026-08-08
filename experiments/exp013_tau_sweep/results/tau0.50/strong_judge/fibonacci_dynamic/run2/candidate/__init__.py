import builtins; import pytest; builtins.pytest = pytest

def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {1: 0, 2: 1}
    def _fibonacci(n):
        if n in memo:
            return memo[n]
        memo[n] = _fibonacci(n - 1) + _fibonacci(n - 2)
        return memo[n]
    return _fibonacci(n)