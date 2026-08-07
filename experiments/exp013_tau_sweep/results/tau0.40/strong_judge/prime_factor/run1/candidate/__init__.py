'''The solution package.'''

__version__ = "0.1.0"

def prime_factors(n):
    if n < 2:
        return []
    factors = []
    for i in range(2, int(n**0.5) + 1):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 1:
        factors.append(n)
    return factors
