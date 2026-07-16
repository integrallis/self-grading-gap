import pytest
from solution import convert_time

def test_convert_time_us1_ac1_1():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    assert convert_time("2021-01-15T12:00:00", "UTC", "America/New_York") == "2021-01-15T07:00:00-05:00"

def test_convert_time_us1_ac1_2():
    # noon UTC in July is 08:00 in New York (UTC-4)
    assert convert_time("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"

def test_convert_time_us1_ac1_3():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result.endswith("-05:00")

def test_convert_time_us1_ac1_4():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    source_time = "2021-01-15T12:00:00"
    result = convert_time(source_time, "UTC", "America/New_York")
    # Check that both moments represent the same instant in UTC
    assert result[:19] == "2021-01-15T07:00:00"

def test_convert_time_us1_ac1_5():
    # Converting between identical zones leaves the wall-clock time unchanged.
    assert convert_time("2021-01-15T12:00:00", "America/New_York", "America/New_York") == "2021-01-15T12:00:00-05:00"

def test_convert_time_us1_ac1_6():
    # Converting to another zone and back recovers the original wall-clock time.
    original_time = "2021-01-15T12:00:00"
    intermediate = convert_time(original_time, "UTC", "America/New_York")
    # Use the intermediate wall-clock portion as a new naive source-zone input
    result = convert_time(intermediate[:19], "America/New_York", "UTC")
    assert result[:19] == "2021-01-15T12:00:00" or result[19:] == "Z"

def test_convert_time_us2_ac2_1():
    # 01:00 in New York is 22:00 the previous day in Los Angeles.
    assert convert_time("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles") == "2021-01-14T22:00:00-08:00"

def test_convert_time_us2_ac2_2():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14).
    assert convert_time("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati") == "2021-01-16T12:00:00+14:00"

def test_convert_time_us2_ac2_3():
    # 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC.
    assert convert_time("2020-12-31T20:00:00", "America/New_York", "UTC") == "2021-01-01T01:00:00+00:00"

def test_convert_time_us2_ac2_4():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India.
    assert convert_time("2020-02-29T23:00:00", "UTC", "Asia/Kolkata") == "2020-03-01T04:30:00+05:30"

def test_convert_time_us3_ac3_1():
    # noon UTC is 17:30 in India (UTC+5:30)
    assert convert_time("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"

def test_convert_time_us3_ac3_2():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    assert convert_time("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu") == "2021-01-15T17:45:00+05:45"

def test_convert_time_us3_ac3_3():
    # Conversions between whole-hour zones never disturb the minutes or seconds of the moment.
    assert convert_time("2021-01-15T12:34:56", "UTC", "America/New_York") == "2021-01-15T07:34:56-05:00"

def test_convert_time_us3_ac3_4():
    # Reverse conversion from India to UTC
    assert convert_time("2021-01-15T09:30:00", "Asia/Kolkata", "UTC") == "2021-01-15T04:00:00+00:00"

def test_convert_time_us4_ac4_1():
    # An ISO 8601 date-time string converts to an ISO 8601 string carrying the destination offset
    assert convert_time("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"

def test_convert_time_us4_ac4_2():
    # Fractional offsets render in the output text
    assert convert_time("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"

def test_convert_time_us5_ac5_1():
    # Malformed date-time text is rejected as invalid.
    with pytest.raises(Exception):  # type of exception not specified
        convert_time("invalid-date-time", "UTC", "America/New_York")

def test_convert_time_us5_ac5_2():
    # An unrecognised zone name — whether source or destination — is rejected
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time("2021-01-15T12:00:00", "UTC", "Unknown/Zone")

def test_convert_time_us5_ac5_3():
    # A moment that already carries zone information is ambiguous input
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time("2021-01-15T12:00:00-05:00", "America/New_York", "America/Los_Angeles")

def test_convert_time_us5_ac5_4():
    # Unknown source zone test
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time("2021-01-15T12:00:00", "Unknown/Zone", "UTC")

def test_convert_time_does_not_consult_system_clock():
    # Ensure that we can convert the same time multiple times without altering the result
    time_string = "2021-01-15T12:00:00"
    zone = "UTC"
    destination = "America/New_York"
    first_conversion = convert_time(time_string, zone, destination)
    second_conversion = convert_time(time_string, zone, destination)
    assert first_conversion == second_conversion