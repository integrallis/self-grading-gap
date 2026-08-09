import pytest

from solution import convert_time_zone  # Assuming the implementation will provide this function.

def test_convert_time_zone_noon_utc_to_new_york_january():
    # noon UTC (15 January 2021) is 07:00 in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_noon_utc_to_new_york_july():
    # noon UTC in July is 08:00 in New York (UTC-4)
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_new_york_to_utc():
    # 07:00 in New York (UTC-5) is noon UTC (15 January 2021)
    result = convert_time_zone("2021-01-15T07:00:00", "America/New_York", "UTC")
    assert result in ["2021-01-15T12:00:00Z", "2021-01-15T12:00:00+00:00"]

def test_convert_time_zone_identical_zones():
    # Converting between identical zones leaves the wall-clock time unchanged
    result = convert_time_zone("2021-01-15T07:00:00", "America/New_York", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_new_york_to_los_angeles():
    # 01:00 in New York is 22:00 the previous day in Los Angeles (UTC-8)
    result = convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles")
    assert result == "2021-01-14T22:00:00-08:00"

def test_convert_time_zone_honolulu_to_kiritimati():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    result = convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati")
    assert result == "2021-01-16T12:00:00+14:00"

def test_convert_time_zone_new_year_boundary():
    # 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC
    result = convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC")
    assert result in ["2021-01-01T01:00:00Z", "2021-01-01T01:00:00+00:00"]

def test_convert_time_zone_leap_day():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India (UTC+5:30)
    result = convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata")
    assert result == "2020-03-01T04:30:00+05:30"

def test_convert_time_zone_fractional_hour_india():
    # noon UTC is 17:30 in India (UTC+5:30)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_fractional_hour_nepal():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu")
    assert result == "2021-01-15T17:45:00+05:45"

def test_convert_time_zone_india_to_utc():
    # 09:30 in India (UTC+5:30) is 04:00 UTC
    result = convert_time_zone("2021-01-15T09:30:00", "Asia/Kolkata", "UTC")
    assert result in ["2021-01-15T04:00:00Z", "2021-01-15T04:00:00+00:00"]

def test_convert_time_zone_whole_hour_zones():
    # 01:23:45 in New York (UTC-5) should yield 06:23:45 in UTC (no change in minutes/seconds)
    result = convert_time_zone("2021-01-15T01:23:45", "America/New_York", "UTC")
    assert result in ["2021-01-15T06:23:45Z", "2021-01-15T06:23:45+00:00"]

def test_convert_time_zone_invalid_iso_format():
    # Malformed date-time text is rejected as invalid
    with pytest.raises(Exception, match=""):
        convert_time_zone("not-a-date-time", "UTC", "America/New_York")

def test_convert_time_zone_unknown_zone_source():
    # An unrecognised source zone name is rejected with an error
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "Unknown/Zone", "America/New_York")

def test_convert_time_zone_unknown_zone_destination():
    # An unrecognised destination zone name is rejected with an error
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")

def test_convert_time_zone_naive_moment():
    # A moment that already carries zone information should be rejected
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "UTC")

def test_convert_time_zone_round_trip():
    # Converting to another zone and back recovers the original wall-clock time
    naive_time = "2021-01-15T07:00:00"
    # Convert from New York to UTC
    result = convert_time_zone(naive_time, "America/New_York", "UTC")
    # Convert back to New York
    result_back = convert_time_zone(result, "UTC", "America/New_York")
    assert result_back == "2021-01-15T07:00:00-05:00"  # Should return the original naive time in New York