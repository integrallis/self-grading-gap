def fibonacci(n):
    if n < 1:
        raise ValueError("Fibonacci sequence is not defined for negative numbers")
    memo = {}
    def fib_helper(x):
        if x in memo:
            return memo[x]
        if x == 1:
            return 0
        elif x == 2:
            return 1
        else:
            memo[x] = fib_helper(x - 1) + fib_helper(x - 2)
            return memo[x]
    return fib_helper(n)