import math

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def announce_number(n):
    if n == 0:
        return "0"
    elif n < 0:
        return str(n)
    elif n % 2 == 0:
        return "Even"
    elif n == 1:
        return "Odd"
    elif is_prime(n):
        return str(n)
    else:
        return "Odd"


def announce_range(start, end):
    if start > end:
        return ""
    return ' '.join(announce_number(n) for n in range(start, end + 1))
