from datetime import datetime, timedelta
import pytest

def last_sundays_of_year(year):
    last_sundays = []
    for month in range(1, 13):
        last_sunday = last_sunday_of_month(year, month)
        last_sundays.append(last_sunday)
    return last_sundays

def last_sunday_of_month(year, month):
    if month < 1 or month > 12:
        raise ValueError('month must be in 1..12')
    # Find the last day of the month
    last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, month, 1) - timedelta(days=1)
    # Calculate the last Sunday
    days_to_subtract = (last_day.weekday() + 1) % 7
    last_sunday = last_day - timedelta(days=days_to_subtract)
    return last_sunday.strftime('%Y-%m-%d')
