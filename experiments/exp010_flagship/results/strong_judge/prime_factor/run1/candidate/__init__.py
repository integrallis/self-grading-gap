'''The solution package.'''

__version__ = "0.1.0"

def prime_factors(n):
    factors = []
    # Start with the smallest prime factor
    divisor = 2
    while n > 1:
        while n % divisor == 0:
            factors.append(divisor)
            n //= divisor
        divisor += 1
    return factors
