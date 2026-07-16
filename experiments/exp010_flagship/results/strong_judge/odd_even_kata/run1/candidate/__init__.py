def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def announce_single(number):
    if number == 0:
        return "0"
    elif number > 0:
        if number % 2 == 0:
            return "Even"
        elif number == 1:
            return "Odd"
        elif is_prime(number):
            return str(number)
        else:
            return "Odd"
    else:
        return str(number)


def announce_range(start, end):
    if start > end:
        return ""
    if start < 0:
        start = 1
    announcements = []
    for number in range(start, end + 1):
        announcements.append(announce_single(number))
    return " ".join(announcements)