from solution import convert_time_zone

def test_convert_time_zone_us1_ac1_1():
    # noon UTC on 15 January 2021 is 07:00 that day in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_us1_ac1_2():
    # noon UTC in July is 08:00 in New York (UTC-4)
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_us1_ac1_3():
    # noon UTC on 15 January 2021 converts to 07:00 in New York (UTC-5)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"
    # Check that the result carries the correct UTC offset
    assert result.endswith("-05:00")

def test_convert_time_zone_us1_ac1_4():
    # Converting should denote the same instant in time
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"
    # Check the original time in UTC
    original_time = "2021-01-15T12:00:00"
    assert convert_time_zone(result, "America/New_York", "UTC") == original_time

def test_convert_time_zone_us1_ac1_5():
    # Converting between identical zones leaves the wall-clock time unchanged
    result = convert_time_zone("2021-01-15T12:00:00", "America/New_York", "America/New_York")
    assert result == "2021-01-15T12:00:00-05:00"

def test_convert_time_zone_us1_ac1_6():
    # Converting to another zone and back recovers the original wall-clock time
    original_time = "2021-01-15T12:00:00"
    result = convert_time_zone(original_time, "UTC", "America/New_York")
    back_to_utc = convert_time_zone(result, "America/New_York", "UTC")
    assert back_to_utc == original_time

def test_convert_time_zone_us2_ac2_1():
    # 01:00 in New York is 22:00 the previous day in Los Angeles
    result = convert_time_zone("2021-01-15T01:00:00", "America/New_York", "America/Los_Angeles")
    assert result == "2021-01-14T22:00:00-08:00"

def test_convert_time_zone_us2_ac2_2():
    # noon in Honolulu (UTC-10) is noon the next day in Kiritimati (UTC+14)
    result = convert_time_zone("2021-01-15T12:00:00", "Pacific/Honolulu", "Pacific/Kiritimati")
    assert result == "2021-01-16T12:00:00+14:00"

def test_convert_time_zone_us2_ac2_3():
    # 20:00 on 31 December 2020 in New York is 01:00 on 1 January 2021 in UTC
    result = convert_time_zone("2020-12-31T20:00:00", "America/New_York", "UTC")
    assert result == "2021-01-01T01:00:00Z"

def test_convert_time_zone_us2_ac2_4():
    # 23:00 UTC on 29 February 2020 is 04:30 on 1 March in India
    result = convert_time_zone("2020-02-29T23:00:00", "UTC", "Asia/Kolkata")
    assert result == "2020-03-01T04:30:00+05:30"

def test_convert_time_zone_us3_ac3_1():
    # noon UTC is 17:30 in India (UTC+5:30)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_us3_ac3_2():
    # noon UTC is 17:45 in Nepal (UTC+5:45)
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kathmandu")
    assert result == "2021-01-15T17:45:00+05:45"

def test_convert_time_zone_us3_ac3_3():
    # Conversions between whole-hour zones never disturb the minutes or seconds
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-01-15T07:00:00-05:00"

def test_convert_time_zone_us4_ac4_1():
    # An ISO 8601 date-time string converts to an ISO 8601 string carrying the destination offset
    result = convert_time_zone("2021-07-15T12:00:00", "UTC", "America/New_York")
    assert result == "2021-07-15T08:00:00-04:00"

def test_convert_time_zone_us4_ac4_2():
    # Fractional offsets render in the output text
    result = convert_time_zone("2021-01-15T12:00:00", "UTC", "Asia/Kolkata")
    assert result == "2021-01-15T17:30:00+05:30"

def test_convert_time_zone_us5_ac5_1():
    # Malformed date-time text is rejected as invalid
    with pytest.raises(ValueError, match="invalid isoformat"):
        convert_time_zone("not-a-date", "UTC", "America/New_York")

def test_convert_time_zone_us5_ac5_2():
    # An unrecognised zone name is rejected
    with pytest.raises(ValueError, match="unknown time zone"):
        convert_time_zone("2021-01-15T12:00:00", "UTC", "Unknown/Zone")

def test_convert_time_zone_us5_ac5_3():
    # A moment that already carries zone information is ambiguous input
    with pytest.raises(ValueError, match="moment must be naive"):
        convert_time_zone("2021-01-15T12:00:00-05:00", "America/New_York", "America/Los_Angeles")