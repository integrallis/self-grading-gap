import pytest
from solution import convert_time_zone  # Assuming the public API is defined in the solution package

def test_convert_local_time_between_zones():
    # AC-1.1: noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York") == "2021-01-15T07:00:00-05:00"
    
    # AC-1.2: noon UTC in July is 08:00 in New York (UTC-4)
    assert convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"
    
    # AC-1.3: the converted result knows its zone
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York") == "2021-01-15T07:00:00-05:00"
    
    # AC-1.4: the source moment and the converted result denote the same instant in time
    assert convert_time_zone("2021-01-15T07:00:00", "America/New_York", "UTC") == "2021-01-15T12:00:00+00:00"
    
    # AC-1.5: converting between identical zones leaves the wall-clock time unchanged
    assert convert_time_zone("2021-01-15T07:00:00", "America/New_York", "America/New_York") == "2021-01-15T07:00:00-05:00"
    
    # AC-1.6: converting to another zone and back recovers the original wall-clock time
    utc_time = convert_time_zone("2021-01-15T07:00:00", "America/New_York", "UTC")
    assert convert_time_zone(utc_time, "UTC", "America/New_York") == "2021-01-15T07:00:00-05:00"

def test_handle_calendar_boundaries():
    # AC-2.1: 01:00 in New York is 22:00 the previous day in Los Angeles
    assert convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles") == "2021-01-14T22:00:00-08:00"
    
    # AC-2.2: noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    assert convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati") == "2021-01-16T12:00:00+14:00"
    
    # AC-2.3: 20:00 on 31 December 2020 in New York is already 01:00 on 1 January 2021 in UTC
    assert convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC") == "2021-01-01T01:00:00+00:00"
    
    # AC-2.4: 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India
    assert convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata") == "2020-03-01T04:30:00+05:30"

def test_support_fractional_hour_zones():
    # AC-3.1: noon UTC is 17:30 in India (UTC+5:30)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"
    
    # Reverse check for AC-3.1: 09:30 in India is 04:00 UTC
    assert convert_time_zone("2021-01-15T09:30:00", "Asia/Kolkata", "UTC") == "2021-01-15T04:00:00+00:00"
    
    # AC-3.2: noon UTC is 17:45 in Nepal (UTC+5:45)
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu") == "2021-01-15T17:45:00+05:45"
    
    # AC-3.3: conversions between whole-hour zones never disturb the minutes or seconds of the moment
    assert convert_time_zone("2021-01-15T12:30:45", "UTC", "America/New_York") == "2021-01-15T07:30:45-05:00"

def test_convert_iso_8601_text():
    # AC-4.1: ISO 8601 date-time string from UTC to New York
    assert convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York") == "2021-07-15T08:00:00-04:00"
    
    # AC-4.2: Fractional offsets render in the output text: UTC noon to India
    assert convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata") == "2021-01-15T17:30:00+05:30"

def test_reject_ambiguous_or_unknown_input():
    # AC-5.1: Malformed date-time text is rejected as invalid.
    with pytest.raises(Exception):
        convert_time_zone("invalid-date-time", "UTC", "America/New_York")
        
    # AC-5.2: An unrecognised zone name is rejected
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")

    # Testing unknown source zone
    with pytest.raises(Exception, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "Unknown/Zone", "America/New_York")
        
    # AC-5.3: A moment that already carries zone information is ambiguous input
    with pytest.raises(Exception, match=r"^moment must be naive"):
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "America/New_York")