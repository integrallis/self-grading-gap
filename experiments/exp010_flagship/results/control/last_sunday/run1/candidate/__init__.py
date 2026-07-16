from datetime import datetime, timedelta

def last_sundays(year, month=None):
    if month is not None:
        if month < 1 or month > 12:
            raise ValueError("month must be in 1..12")
        # Get the last day of the month
        last_day = datetime(year, month + 1, 1) - timedelta(days=1) if month < 12 else datetime(year, month, 31)
    else:
        last_day = datetime(year, 12, 31)

    # Get the last Sunday of the month
    last_sunday = last_day - timedelta(days=(last_day.weekday() + 1) % 7)

    if month:
        return last_sunday.strftime('%Y-%m-%d')

    return [
        (datetime(year, m + 1, 1) - timedelta(days=1) - timedelta(days=(datetime(year, m + 1, 1) - timedelta(days=1)).weekday() + 1)).strftime('%Y-%m-%d')
        for m in range(1, 13)
    ]
