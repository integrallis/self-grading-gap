from datetime import datetime
import pytz

def convert_time_zone(time_str, from_zone, to_zone):
    # Validate and parse the input time string
    try:
        if 'Z' in time_str:
            naive_time = datetime.strptime(time_str[:-1], '%Y-%m-%dT%H:%M:%S')
            utc_time = pytz.utc.localize(naive_time)
        else:
            naive_time = datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%S')
            utc_time = pytz.timezone(from_zone).localize(naive_time)
    except ValueError:
        raise ValueError("invalid date-time text")

    # Validate the time zones
    try:
        from_tz = pytz.timezone(from_zone)
        to_tz = pytz.timezone(to_zone)
    except pytz.UnknownTimeZoneError:
        raise ValueError("unknown time zone")

    # Convert the time to the target time zone
    target_time = utc_time.astimezone(to_tz)

    # Check if the input time was naive
    if from_zone == to_zone:
        if naive_time.tzinfo is not None:
            raise ValueError("moment must be naive")

    # Return the time in the required format with the timezone offset
    return target_time.strftime('%Y-%m-%dT%H:%M:%S%z')[:-2] + ':' + target_time.strftime('%z')[-2:] if target_time.tzinfo else target_time.strftime('%Y-%m-%dT%H:%M:%S')
