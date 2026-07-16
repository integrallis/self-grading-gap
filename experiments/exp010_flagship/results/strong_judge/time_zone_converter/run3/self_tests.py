import pytest
from solution import convert_time_zone

def test_convert_local_time_us_1_1():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_local_time_us_1_2():
    # noon UTC in July is 08:00 in New York (UTC-4)
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_local_time_us_1_3():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result.endswith("-05:00")

def test_convert_local_time_us_1_4():
    # Input has offset; should be rejected
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time_zone("2021-01-15T07:00:00-05:00", "America/New_York", "UTC")

def test_convert_local_time_us_1_5():
    # Converting between identical zones leaves the wall-clock time unchanged.
    result = convert_time_zone("2021-01-15T12:00:00", "America/New_York", "America/New_York")
    assert result == "2021-01-15T12:00:00-05:00"

def test_convert_local_time_us_1_6():
    # Input has offset; should be rejected
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time_zone("2021-01-15T07:00:00-05:00", "America/New_York", "UTC")

def test_calendar_boundaries_us_2_1():
    # 01:00 in New York is 22:00 the previous day in Los Angeles
    result = convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles")
    assert result == "2021-01-14T22:00:00-08:00"

def test_calendar_boundaries_us_2_2():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    result = convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati")
    assert result == "2021-01-16T12:00:00+14:00"

def test_calendar_boundaries_us_2_3():
    # 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC
    result = convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC")
    assert result in ["2021-01-01T01:00:00Z", "2021-01-01T01:00:00+00:00"]

def test_calendar_boundaries_us_2_4():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India
    result = convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata")
    assert result == "2020-03-01T04:30:00+05:30"

def test_fractional_hour_zones_us_3_1():
    # noon UTC is 17:30 in India (UTC+5:30)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_fractional_hour_zones_us_3_1_reverse():
    # 09:30 in India is 04:00 UTC
    result = convert_time_zone("2021-01-15T09:30:00", "Asia/Kolkata", "UTC")
    assert result == "2021-01-15T04:00:00Z"  # Accept either Z or +00:00

def test_fractional_hour_zones_us_3_2():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu")
    assert result == "2021-01-15T17:45:00+05:45"

def test_fractional_hour_zones_us_3_3():
    # Conversions between whole-hour zones never disturb the minutes or seconds of the moment.
    result = convert_time_zone("2021-01-15T12:30:45", "America/New_York", "UTC")
    assert result in ["2021-01-15T17:30:45Z", "2021-01-15T17:30:45+00:00"]

def test_convert_iso_8601_text_us_4_1():
    # An ISO 8601 date-time string converts to an ISO 8601 string carrying the destination offset
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_iso_8601_text_us_4_2():
    # Fractional offsets render in the output text
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_reject_malformed_datetime_us_5_1():
    # Malformed date-time text is rejected as invalid
    with pytest.raises(Exception):
        convert_time_zone("invalid-date", "UTC", "America/New_York")

def test_reject_unknown_source_zone_us_5_2():
    # An unrecognised source zone name is rejected with an error
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "Unknown/Zone", "America/New_York")

def test_reject_unknown_destination_zone_us_5_3():
    # An unrecognised destination zone name is rejected with an error
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")

def test_reject_ambiguous_input_us_5_4():
    # A moment that already carries zone information is ambiguous input and is rejected
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "America/New_York")