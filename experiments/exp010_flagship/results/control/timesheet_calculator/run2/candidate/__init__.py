import re

__version__ = "0.1.0"

def parse_time(time_str):
    time_str = time_str.strip().upper()
    match = re.match(r'^(\d{1,2}):(\d{2})(?:\s*(AM|PM))?$', time_str)
    if not match:
        match = re.match(r'^(\d{1,2})(\d{2})(?:\s*(AM|PM))?$', time_str)
    if match:
        groups = match.groups()
        if len(groups) == 2:
            hour, minute = groups[0], groups[1]
            period = ''
        elif len(groups) == 3:
            hour, minute, period = groups
        else:
            raise ValueError(f"Invalid time: '{time_str}'")
        hour = int(hour)
        minute = int(minute)
        if minute >= 60:
            raise ValueError("Invalid time")
        if hour < 0 or hour > 23:
            raise ValueError("Invalid time")
        if period:
            if hour > 12:
                raise ValueError(f"Invalid time: '{time_str}'")
            if period == 'PM' and hour != 12:
                hour += 12
            if period == 'AM' and hour == 12:
                hour = 0
        return hour, minute
    raise ValueError(f"Invalid time: '{time_str}'")

def calculate_worked_hours(start, end, break_time=None):
    start_hour, start_minute = parse_time(start)
    end_hour, end_minute = parse_time(end)

    start_total_minutes = start_hour * 60 + start_minute
    end_total_minutes = end_hour * 60 + end_minute

    if end_total_minutes < start_total_minutes:
        end_total_minutes += 24 * 60

    worked_minutes = end_total_minutes - start_total_minutes

    if break_time:
        break_hour, break_minute = parse_time(break_time)
        break_total_minutes = break_hour * 60 + break_minute
        if break_total_minutes > worked_minutes:
            raise ValueError("Break duration exceeds time worked")
        worked_minutes -= break_total_minutes

    if worked_minutes < 0:
        worked_minutes = 0

    worked_hours = worked_minutes // 60
    worked_minutes = worked_minutes % 60

    return f'{worked_hours:02}:{worked_minutes:02}'
