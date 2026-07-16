# file: datetime.py

from datetime import date as Date
from datetime import timedelta as Timedelta

def date(year, month, day):
    return Date(year, month, day)

def timedelta(days):
    return Timedelta(days)
