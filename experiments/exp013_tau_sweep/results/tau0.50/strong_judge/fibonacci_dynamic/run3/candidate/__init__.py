def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {1: 0, 2: 1}
    def fib_memoized(x):
        if x in memo:
            return memo[x]
        memo[x] = fib_memoized(x - 1) + fib_memoized(x - 2)
        return memo[x]
    return fib_memoized(n)