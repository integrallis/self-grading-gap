def announce_number(n):
    if n == 0:
        return "0"
    elif n > 0:
        if n % 2 == 0:
            return "Even"
        else:
            return str(n) if is_prime(n) else "Odd"
    else:
        return str(n)


def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True


def announce_range(start, end):
    if start > end:
        return ""
    result = []
    for i in range(1 if start < 0 else start, end + 1):
        result.append(announce_number(i))
    return " ".join(result)