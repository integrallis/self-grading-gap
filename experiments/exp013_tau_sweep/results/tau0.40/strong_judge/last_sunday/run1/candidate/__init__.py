import calendar
from datetime import datetime, timedelta

def last_sundays(year, month=None):
    if month is not None:
        if month < 1 or month > 12:
            raise ValueError('month must be in 1..12')
        last_day = calendar.monthrange(year, month)[1]  # Get last day of the month
        last_date = datetime(year, month, last_day)
        # Find the last Sunday of the specific month
        last_sunday = last_date - timedelta(days=(last_date.weekday() + 1) % 7)
        return last_sunday.strftime('%Y-%m-%d')
    else:
        last_dates = []
        for m in range(1, 13):
            last_day = calendar.monthrange(year, m)[1]
            last_date = datetime(year, m, last_day)
            # Find the last Sunday of the month
            last_sunday = last_date - timedelta(days=(last_date.weekday() + 1) % 7)
            last_dates.append(last_sunday.strftime('%Y-%m-%d'))
        return last_dates