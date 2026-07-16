def prime_factor_decomposition(n):
    factors = []
    # Handle the case for 1
    if n == 1:
        return factors
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    # n must be odd at this point, so a skip of 2 (i.e., check only odd numbers) is fine
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    # This condition is to check if n is a prime number greater than 2
    if n > 2:
        factors.append(n)
    return factors
