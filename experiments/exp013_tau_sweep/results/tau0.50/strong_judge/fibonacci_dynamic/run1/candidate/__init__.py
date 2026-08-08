def fibonacci(n, memo={}) -> int:
    if n < 1:
        raise Exception("Fibonacci sequence is not defined for negative numbers")
    if n in memo:
        return memo[n]
    if n == 1:
        return 0
    elif n == 2:
        return 1
    else:
        memo[n] = fibonacci(n - 1, memo) + fibonacci(n - 2, memo)
        return memo[n]