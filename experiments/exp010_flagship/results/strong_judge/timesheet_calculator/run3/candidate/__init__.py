import re
from datetime import timedelta

def calculate_worked_hours(start_time: str, end_time: str, break_time: str = '00:00') -> str:
    def parse_time(time_str):
        # Handle 12-hour format
        match = re.match(r'^\d{1,2}:\d{2}\s*([AaPp][Mm]|[Pp][Mm])?$', time_str)
        if match:
            hour, minute, period = match.groups()
            hour = int(hour)
            minute = int(minute)
            if period:
                if period.lower() == 'pm' and hour != 12:
                    hour += 12
                if period.lower() == 'am' and hour == 12:
                    hour = 0
                if hour < 1 or hour > 12:
                    raise Exception(f"Invalid time: '{time_str}')
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise Exception(f'Invalid time: {time_str}')
            return hour, minute
        # Handle compact 24-hour format
        match = re.match(r'^\d{3,4}$', time_str)
        if match:
            hour = int(time_str[:-2])
            minute = int(time_str[-2:])
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise Exception(f'Invalid time: {time_str}')
            return hour, minute
        # Handle 24-hour format
        match = re.match(r'^\d{1,2}(?::(\d{2}))?$', time_str)
        if match:
            hour = int(match.group(1))
            minute = int(match.group(2) or '0')
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                raise Exception('Invalid time')
            return hour, minute
        raise Exception(f'Invalid time: {time_str}')

    def format_duration(duration):
        hours, remainder = divmod(duration.total_seconds() // 60, 60)
        return f'{int(hours):02}:{int(remainder):02}'

    # Parse start and end times
    start_hour, start_minute = parse_time(start_time)
    end_hour, end_minute = parse_time(end_time)

    # Calculate worked time
    start = timedelta(hours=start_hour, minutes=start_minute)
    end = timedelta(hours=end_hour, minutes=end_minute)
    if end < start:
        end += timedelta(days=1)  # Account for overnight shift

    worked_time = end - start

    # Parse break time
    break_hour, break_minute = parse_time(break_time)
    break_duration = timedelta(hours=break_hour, minutes=break_minute)

    if break_duration > worked_time:
        raise Exception('Break duration exceeds time worked')

    total_worked = worked_time - break_duration
    return format_duration(total_worked)