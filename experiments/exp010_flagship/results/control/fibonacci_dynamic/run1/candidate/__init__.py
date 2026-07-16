def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {1: 0, 2: 1}
    def fib_helper(x):
        if x in memo:
            return memo[x]
        memo[x] = fib_helper(x - 1) + fib_helper(x - 2)
        return memo[x]
    return fib_helper(n)