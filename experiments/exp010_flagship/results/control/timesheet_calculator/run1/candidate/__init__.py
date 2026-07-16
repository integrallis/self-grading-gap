import re
from datetime import datetime, timedelta

def parse_time(time_str):
    time_str = time_str.upper()  # Standardize AM/PM notation
    # Handle 12-hour AM/PM format
    if 'AM' in time_str or 'PM' in time_str:
        time_str = time_str.replace('AM', '').replace('PM', '').strip()
        time_format = '%I:%M'
        if 'PM' in time_str:
            hour, minute = map(int, time_str.split(':'))
            if hour != 12:
                hour += 12
            time_str = f'{hour:02}:{minute:02}'
    else:
        time_format = '%H:%M'
    # Handle compact time notation
    if len(time_str) <= 4:
        time_str = time_str.zfill(4)
        time_str = f'{time_str[:-2]}:{time_str[-2:]}'
    # Validate time format
    try:
        return datetime.strptime(time_str, time_format)
    except ValueError:
        raise ValueError(f'Invalid time: {time_str}')

def calculate_worked_hours(start, end, break_time='00:00'):
    start_time = parse_time(start)
    end_time = parse_time(end)
    break_duration = parse_time(break_time) if break_time != '00:00' else timedelta(hours=0)
    
    # Handle overnight shift
    if end_time < start_time:
        end_time += timedelta(days=1)

    worked_duration = end_time - start_time - timedelta(hours=break_duration.hour, minutes=break_duration.minute)

    if worked_duration < timedelta():
        raise ValueError('Break duration exceeds time worked')

    hours, remainder = divmod(int(worked_duration.total_seconds() // 60), 60)
    return f'{hours:02}:{remainder:02}'