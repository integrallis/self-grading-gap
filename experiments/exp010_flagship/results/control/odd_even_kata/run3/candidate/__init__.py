def announce_number(n):
    if n == 0:
        return "0"
    elif n == 1:
        return "Odd"
    elif n % 2 == 0:
        return "Even" if n > 0 else str(n)
    else:
        return str(n)


def announce_range(start, end):
    if start > end:
        return ""
    return " ".join(announce_number(i) for i in range(start, end + 1) if (i > 0 or i == 0 or i % 2 != 0))