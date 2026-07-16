import pytz
from datetime import datetime

def convert_time_zone(iso_datetime: str, from_zone: str, to_zone: str) -> str:
    # Parse the input datetime string
    try:
        naive_datetime = datetime.fromisoformat(iso_datetime)
    except ValueError:
        raise ValueError('invalid isoformat')
    if naive_datetime.tzinfo is not None:
        raise ValueError('moment must be naive')

    # Get the timezone objects
    try:
        from_tz = pytz.timezone(from_zone)
        to_tz = pytz.timezone(to_zone)
    except pytz.UnknownTimeZoneError:
        raise ValueError('unknown time zone')

    # Localize the naive datetime to the from_zone
    localized_datetime = from_tz.localize(naive_datetime)
    # Convert to the target timezone
    target_datetime = localized_datetime.astimezone(to_tz)

    # Format the output string with the correct offset
    return target_datetime.isoformat()