def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

def announce_number(num):
    if num == 0:
        return "0"
    elif num < 0:
        if num % 2 == 0:
            return str(num)
        else:
            return str(num)
    elif num == 1:
        return "Odd"
    elif num % 2 == 0:
        return "Even"
    elif is_prime(num):
        return str(num)
    else:
        return "Odd"


def announce_range(start, end):
    if start > end:
        return ""
    return " ".join(announce_number(i) for i in range(start, end + 1))