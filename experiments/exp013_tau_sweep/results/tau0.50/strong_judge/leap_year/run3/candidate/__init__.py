def is_leap_year(year):
    # A year is a leap year if it is divisible by 4,
    # but not divisible by 100 unless it is also divisible by 400.
    if year % 400 == 0:
        return True
    if year % 100 == 0:
        return False
    if year % 4 == 0:
        return True
    return False
