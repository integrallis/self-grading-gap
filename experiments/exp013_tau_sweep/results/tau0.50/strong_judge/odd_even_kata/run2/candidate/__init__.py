def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def announce_number(n):
    if n == 0:
        return "0"
    elif n % 2 == 0:
        return "Even" if n > 0 else str(n)
    elif n < 0:
        return str(n)
    elif n == 1:
        return "Odd"
    else:
        return str(n) if is_prime(n) else "Odd"


def announce_range(start, end):
    if start > end:
        return ""
    if start < 0:
        start = 1
    return " ".join(announce_number(i) for i in range(start, end + 1))
