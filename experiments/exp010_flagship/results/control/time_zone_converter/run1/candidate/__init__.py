import pytz
from datetime import datetime

def convert_time_zone(dt_str, from_zone, to_zone):
    # Parse the input datetime string
    try:
        if dt_str.endswith('Z'):
            dt = datetime.strptime(dt_str[:-1], '%Y-%m-%dT%H:%M:%S')
        else:
            dt = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        raise ValueError('invalid date-time format')

    # Get the timezone objects
    try:
        from_tz = pytz.timezone(from_zone)
        to_tz = pytz.timezone(to_zone)
    except pytz.UnknownTimeZoneError:
        raise ValueError('unknown time zone')

    # Localize the datetime to the from_zone
    if dt.tzinfo is not None:
        raise ValueError('moment must be naive')
    localized_dt = from_tz.localize(dt)

    # Convert to the target timezone
    target_dt = localized_dt.astimezone(to_tz)

    # Format the output datetime string
    if to_zone == 'UTC':
        return target_dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    return target_dt.strftime('%Y-%m-%dT%H:%M:%S%z')
