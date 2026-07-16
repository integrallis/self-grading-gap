from datetime import datetime, timedelta, time
import re

def parse_time(time_str):
    # Normalize time strings
    time_str = re.sub(r'\s+', '', time_str.strip().lower())
    # Validate time formats
    if not re.match(r'^(0?[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', time_str) and not re.match(r'^\d{1,4}$', time_str):
        raise ValueError('Invalid time')
    # Handle 12-hour format
    if 'am' in time_str or 'pm' in time_str:
        return datetime.strptime(time_str, '%I:%M %p').time()
    # Handle compact digits and 24-hour format
    time_str = re.sub(r'(^|\s)(\d{1,2})(\d{2})$', r'\1\2:\3', time_str)
    return datetime.strptime(time_str, '%H:%M').time()

def calculate_work_hours(clock_in, clock_out, break_duration='00:00'):
    # Parse inputs
    clock_in_time = parse_time(clock_in)
    clock_out_time = parse_time(clock_out)
    if break_duration and break_duration != '00:00':
        break_duration_time = parse_time(break_duration)
    else:
        break_duration_time = time(0, 0)

    # Convert times to datetime for calculation
    today = datetime.today().date()
    clock_in_dt = datetime.combine(today, clock_in_time)
    clock_out_dt = datetime.combine(today, clock_out_time)

    # Handle overnight shifts
    if clock_out_dt < clock_in_dt:
        clock_out_dt += timedelta(days=1)

    # Calculate total worked time
    total_worked = clock_out_dt - clock_in_dt

    # Convert break duration to timedelta
    break_time = timedelta(hours=break_duration_time.hour, minutes=break_duration_time.minute)

    # Check if break exceeds work duration
    if break_time > total_worked:
        raise ValueError('Break duration exceeds time worked')

    # Calculate final worked hours
    final_worked = total_worked - break_time

    # Return result in HH:MM format
    total_minutes = int(final_worked.total_seconds() // 60)
    hours, minutes = divmod(total_minutes, 60)
    return f'{hours:02}:{minutes:02}'
