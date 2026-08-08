import pytest
from solution import convert_time_zone

def test_convert_time_zone_us_1_1():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York") == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_us_1_2():
    # noon UTC in July is 08:00 in New York (UTC-4)
    assert convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_us_1_3():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"  # Verify the output carries the correct UTC offset

def test_convert_time_zone_us_1_4():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    original = "2021-01-15T12:00:00"
    result = convert_time_zone(original, "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"  # Ensure the source moment and the converted result denote the same instant in time

def test_convert_time_zone_us_1_5():
    # Converting between identical zones leaves the wall-clock time unchanged
    assert convert_time_zone("2021-01-15T12:00:00", "America/New_York", "America/New_York") == "2021-01-15T12:00:00-05:00"

def test_convert_time_zone_us_1_6():
    # Converting to another zone and back recovers the original wall-clock time
    original = "2021-01-15T12:00:00"
    intermediate = convert_time_zone(original, "UTC", "America/New_York")
    result = convert_time_zone(intermediate, "America/New_York", "UTC")
    assert result == "2021-01-15T12:00:00+00:00"  # Should recover original wall-clock time

def test_convert_time_zone_us_2_1():
    # 01:00 in New York is 22:00 the previous day in Los Angeles
    assert convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles") == "2021-01-14T22:00:00-08:00"

def test_convert_time_zone_us_2_2():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    assert convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati") == "2021-01-16T12:00:00+14:00"

def test_convert_time_zone_us_2_3():
    # 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC
    assert convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC") == "2021-01-01T01:00:00+00:00"

def test_convert_time_zone_us_2_4():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India
    assert convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata") == "2020-03-01T04:30:00+05:30"

def test_convert_time_zone_us_3_1():
    # noon UTC is 17:30 in India (UTC+5:30)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_us_3_1_reverse():
    # 09:30 in India converts to 04:00 UTC
    assert convert_time_zone("2021-01-15T09:30:00", "Asia/Kolkata", "UTC") == "2021-01-15T04:00:00+00:00"

def test_convert_time_zone_us_3_2():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu") == "2021-01-15T17:45:00+05:45"

def test_convert_time_zone_us_3_3():
    # Conversions between whole-hour zones never disturb the minutes or seconds of the moment
    assert convert_time_zone("2021-01-15T12:30:45", "UTC", "America/New_York") == "2021-01-15T07:30:45-05:00"

def test_convert_time_zone_us_4_1():
    # An ISO 8601 date-time string converts to an ISO 8601 string carrying the destination offset
    assert convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_us_4_2():
    # Fractional offsets render in the output text
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_us_5_1():
    # Malformed date-time text is rejected
    with pytest.raises(Exception):
        convert_time_zone("invalid-date", "UTC", "America/New_York")

def test_convert_time_zone_us_5_2():
    # An unrecognised zone name is rejected with an error containing "unknown time zone"
    with pytest.raises(Exception) as e:
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")
    assert "unknown time zone" in str(e.value)

def test_convert_time_zone_us_5_2_source():
    # An unrecognised source zone name is rejected
    with pytest.raises(Exception) as e:
        convert_time_zone("2021-01-15T12:00:00", "Unknown/Zone", "America/New_York")
    assert "unknown time zone" in str(e.value)

def test_convert_time_zone_us_5_3():
    # A moment that already carries zone information is ambiguous input
    with pytest.raises(Exception) as e:
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "America/Los_Angeles")
    assert str(e.value).startswith("moment must be naive")

def test_convert_time_zone_system_clock_independence():
    # Ensure conversion does not consult the system clock
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Australia/Adelaide") == "2021-01-15T22:30:00+10:30"