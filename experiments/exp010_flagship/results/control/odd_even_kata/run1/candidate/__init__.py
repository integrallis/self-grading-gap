def announce_number(n):
    if n == 0:
        return "0"
    if n > 0 and n % 2 == 0:
        return "Even"
    if n > 0 and is_prime(n):
        return str(n)
    if n < 0:
        return str(n)
    return "Odd"


def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def announce_range(start, end):
    if start > end:
        return ""
    return " ".join(announce_number(i) for i in range(max(0, start), end + 1))