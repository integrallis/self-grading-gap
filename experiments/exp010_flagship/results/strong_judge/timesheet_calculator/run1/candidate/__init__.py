def calculate_work_hours(start, end, break_duration='00:00'):
    import re
    from datetime import datetime, timedelta

    def validate_time_format(time_str):
        if not re.match(r'^(\d{1,2}:\d{2}|\d{1,4}|\d{1,2}\s?[APap][Mm])$', time_str):
            raise Exception(f"Invalid time: '{time_str}'")
        if ':' in time_str:
            hour = int(time_str.split(':')[0])
            minute = int(time_str.split(':')[1])
        else:
            hour = int(time_str[:-2]) if len(time_str) > 2 else int(time_str)
            minute = 0
        if hour < 0 or minute < 0 or minute >= 60:
            raise Exception("Invalid time")
        if len(time_str) <= 4:
            if hour > 23:
                raise Exception("Invalid time")
        else:
            if hour < 1 or hour > 12:
                raise Exception(f"Invalid time: '{time_str}'")

    def parse_time(time_str):
        if re.match(r'\d{1,4}$', time_str):
            if len(time_str) == 4:
                return datetime.strptime(time_str, '%H%M')
            else:
                return datetime.strptime(time_str.zfill(4), '%H%M')
        if re.match(r'\d{1,2}:\d{2}\s?[APap][Mm]$', time_str):
            return datetime.strptime(time_str.strip(), '%I:%M %p')
        return datetime.strptime(time_str, '%H:%M')

    validate_time_format(start)
    validate_time_format(end)
    validate_time_format(break_duration)

    start_time = parse_time(start)
    end_time = parse_time(end)

    if end_time < start_time:
        end_time += timedelta(days=1)

    worked_duration = end_time - start_time

    break_time = parse_time(break_duration)
    break_duration_minutes = break_time.hour * 60 + break_time.minute
    if break_duration_minutes > worked_duration.total_seconds() / 60:
        raise Exception("Break duration exceeds time worked")
    worked_duration -= timedelta(minutes=break_duration_minutes)

    total_minutes = int(worked_duration.total_seconds() / 60)
    hours, minutes = divmod(total_minutes, 60)
    return f'{hours:02}:{minutes:02}'
