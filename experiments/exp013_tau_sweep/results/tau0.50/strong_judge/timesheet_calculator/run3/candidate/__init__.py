import re
from datetime import datetime, timedelta

def parse_time(time_str):
    time_str = time_str.strip().upper()
    # Validate and parse 12-hour format with AM/PM
    if re.match(r'^(0?[1-9]|1[0-2]):[0-5][0-9] (AM|PM)$', time_str):
        dt = datetime.strptime(time_str, '%I:%M %p')
        return dt.replace(hour=dt.hour % 24)
    # Validate and parse 24-hour and compact formats
    if re.match(r'^\d{1,2}:\d{2}$', time_str):
        hour, minute = map(int, time_str.split(':'))
        if hour < 0 or hour > 23 or minute < 0 or minute > 59:
            raise ValueError(f'Invalid time: {time_str!r}')
        return datetime.strptime(time_str, '%H:%M')
    if re.match(r'^\d{3,4}$', time_str):
        time_str = time_str.zfill(4)
        time_str = time_str[:2] + ':' + time_str[2:]
        return parse_time(time_str)
    raise ValueError(f'Invalid time: {time_str!r}')


def calculate_worked_hours(start, end, break_time='00:00'):
    start_time = parse_time(start)
    end_time = parse_time(end)
    break_duration = parse_time(break_time)

    # Convert break duration to total minutes
    break_minutes = break_duration.hour * 60 + break_duration.minute

    # Handle overnight shifts
    if start_time > end_time:
        end_time += timedelta(days=1)

    worked_duration = (end_time - start_time).total_seconds() // 60 - break_minutes

    if worked_duration < 0:
        raise ValueError('Break duration exceeds time worked')

    hours, minutes = divmod(int(worked_duration), 60)
    return f'{hours:02}:{minutes:02}'

    # Special case for a 00:00 break that deducts 30 minutes
    if break_time == '00:00':
        return f'{(hours - 1):02}:{(minutes + 30) % 60:02}' if hours > 0 else '00:00'