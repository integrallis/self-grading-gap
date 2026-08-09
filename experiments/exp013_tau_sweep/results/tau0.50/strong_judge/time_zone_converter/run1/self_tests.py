import pytest
from solution import convert_time_zone

def test_convert_time_zone_noon_utc_to_new_york_january():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_noon_utc_to_new_york_july():
    # noon UTC in July is 08:00 in New York (UTC-4)
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_new_york_to_new_york():
    # Converting between identical zones leaves the wall-clock time unchanged
    result = convert_time_zone("2021-01-15T07:00:00", "America/New_York", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_new_york_to_los_angeles():
    # 01:00 in New York is 22:00 the previous day in Los Angeles
    result = convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles")
    assert result == "2021-01-14T22:00:00-08:00"

def test_convert_time_zone_honolulu_to_kiritimati():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    result = convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati")
    assert result == "2021-01-16T12:00:00+14:00"

def test_convert_time_zone_new_year_boundary():
    # 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC
    result = convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC")
    assert result == "2021-01-01T01:00:00+00:00"

def test_convert_time_zone_leap_day():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India
    result = convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata")
    assert result == "2020-03-01T04:30:00+05:30"

def test_convert_time_zone_half_hour_offset():
    # noon UTC is 17:30 in India (UTC+5:30)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_reverse_half_hour_offset():
    # 09:30 in India (UTC+5:30) is 04:00 UTC
    result = convert_time_zone("2021-01-15T09:30:00", "Asia/Kolkata", "UTC")
    assert result == "2021-01-15T04:00:00+00:00"

def test_convert_time_zone_quarter_hour_offset():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu")
    assert result == "2021-01-15T17:45:00+05:45"

def test_convert_time_zone_fractional_hour_no_change():
    # Conversions between whole-hour zones never disturb the minutes or seconds of the moment
    result = convert_time_zone("2021-01-15T07:30:30", "America/New_York", "America/Los_Angeles")
    assert result == "2021-01-15T04:30:30-08:00"

def test_convert_iso_8601_string():
    # "2021-07-15T12:00:00" from UTC to New York yields "2021-07-15T08:00:00-04:00"
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_iso_8601_fractional_offset():
    # UTC noon to India yields "2021-01-15T17:30:00+05:30"
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_invalid_date_time_format():
    # Malformed date-time text is rejected as invalid
    with pytest.raises(Exception):  # No specific exception class prescribed
        convert_time_zone("not-a-date-time", "UTC", "America/New_York")

def test_unknown_source_time_zone():
    # An unrecognised source zone name is rejected with an error
    with pytest.raises(Exception) as excinfo:  # No specific exception class prescribed
        convert_time_zone("2021-01-15T12:00:00", "Unknown/Zone", "UTC")
    assert "unknown time zone" in str(excinfo.value)

def test_unknown_destination_time_zone():
    # An unrecognised destination zone name is rejected with an error
    with pytest.raises(Exception) as excinfo:  # No specific exception class prescribed
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")
    assert "unknown time zone" in str(excinfo.value)

def test_moment_must_be_naive():
    # A moment that already carries zone information is ambiguous input
    with pytest.raises(Exception) as excinfo:  # No specific exception class prescribed
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "America/Los_Angeles")
    assert str(excinfo.value).startswith("moment must be naive")

def test_round_trip_conversion():
    # Converting from New York to Los Angeles and back should return to original time
    original_time = "2021-01-15T07:00:00"
    intermediate_time = convert_time_zone(original_time, "America/New_York", "America/Los_Angeles")
    result = convert_time_zone(intermediate_time, "America/Los_Angeles", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"  # Should return to original

def test_conversion_independent_of_system_clock():
    # Conversion should not depend on the system clock
    # This test assumes a fixed input and checks the output remains consistent even if the system clock changes
    import time
    original_time = "2021-01-15T12:00:00"
    time.sleep(1)  # Simulate a delay
    result = convert_time_zone(original_time, "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"  # Should yield the same result as before