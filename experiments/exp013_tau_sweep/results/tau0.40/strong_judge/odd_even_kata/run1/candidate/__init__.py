def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def announce_number(n):
    if n == 0:
        return "0"
    if n < 0:
        return str(n)
    if n % 2 == 0:
        return "Even"
    if n == 1:
        return "Odd"
    if is_prime(n):
        return str(n)
    return "Odd"

def announce_range(start, end):
    if start > end:
        return ""
    return ' '.join(announce_number(i) for i in range(start, end + 1))