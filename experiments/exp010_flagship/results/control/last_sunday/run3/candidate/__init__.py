from datetime import datetime, timedelta
import pytest

def last_sundays(year, month=None):
    if month is not None:
        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        return find_last_sunday(year, month)
    return [find_last_sunday(year, m) for m in range(1, 13)]

def find_last_sunday(year, month):
    # Get the last day of the month
    if month in (1, 3, 5, 7, 8, 10):
        last_day = 31
    elif month in (4, 6, 9, 11):
        last_day = 30
    elif month == 2:
        last_day = 29 if (year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)) else 28

    last_date = datetime(year, month, last_day)

    # Find the last Sunday
    while last_date.weekday() != 6:  # 6 is Sunday
        last_date -= timedelta(days=1)

    return last_date.strftime('%Y-%m-%d')