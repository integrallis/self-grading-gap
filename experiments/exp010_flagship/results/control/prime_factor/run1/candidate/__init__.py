'''The solution package.''' 

__version__ = "0.1.0" 

def prime_factors(n):
    factors = []
    # Check for factors of 2
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # Check for odd factors from 3 upwards
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    # If n becomes a prime number greater than 2
    if n > 2:
        factors.append(n)
    return factors