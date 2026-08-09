import pytest
from solution import calculate_work_hours

# US-1: Compute the worked duration of a shift

def test_work_duration_basic():
    # 07:02 to 16:22 = 09:20
    assert calculate_work_hours("07:02", "16:22") == "09:20"

def test_work_duration_with_break():
    # 08:42 to 16:20 with a break of 00:30
    # Total time = 07:38
    # After subtracting break: 07:08
    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"

def test_work_duration_no_break():
    # 08:42 to 16:20 with a break of 00:00
    # Total time = 07:38
    assert calculate_work_hours("08:42", "16:20", "00:00") == "07:38"

def test_work_duration_identical_times():
    # Identical start and end times mean no time worked: 00:00
    assert calculate_work_hours("09:00", "09:00") == "00:00"

def test_work_duration_full_day():
    # 00:00 to 23:59 = 23:59
    assert calculate_work_hours("00:00", "23:59") == "23:59"

def test_work_duration_zero_hours():
    # 09:05 to 09:13 = 00:08
    assert calculate_work_hours("09:05", "09:13") == "00:08"

# US-2: Handle overnight shifts

def test_work_duration_overnight():
    # 23:00 to 01:00 = 02:00
    assert calculate_work_hours("23:00", "01:00") == "02:00"

def test_work_duration_overnight_with_break():
    # 17:02 to 02:09 with a break of 00:35
    # Total time = 09:07
    # After subtracting break: 08:32
    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"

# US-3: Accept flexible time notations

def test_work_duration_compact_notation():
    # "800" to "1530" = 07:30
    assert calculate_work_hours("800", "1530") == "07:30"

def test_work_duration_mixed_notation():
    # "0842" to "1620" with "0030" break = 07:08
    assert calculate_work_hours("0842", "1620", "0030") == "07:08"

def test_work_duration_12_hour_notation():
    # 8:00 AM to 4:30 PM = 08:30
    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"

def test_work_duration_12_hour_midnight():
    # 12:00 AM to 01:00 = 01:00
    assert calculate_work_hours("12:00 AM", "01:00") == "01:00"

def test_work_duration_12_hour_noon():
    # 12:00 PM to 01:00 = 13:00
    assert calculate_work_hours("12:00 PM", "01:00") == "13:00"

def test_work_duration_lowercase_am_pm():
    # 8:00 am to 4:30 pm = 08:30
    assert calculate_work_hours("8:00 am", "4:30 pm") == "08:30"

def test_work_duration_mixed_12_and_24_hour():
    # 8:00 AM to 17:00 = 09:00
    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"

def test_break_12_hour_notation():
    # 06:00 to 23:00 minus 1:00 PM (13:00) = 04:00
    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"

# US-4: Reject invalid times and breaks

def test_invalid_time_hour_out_of_bounds():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("24:00", "01:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_hour_out_of_bounds_high():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("25:00", "01:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_minute_out_of_bounds():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("09:60", "10:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_minute_out_of_bounds_high():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("09:75", "10:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_non_numeric():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("09:00", "ten o'clock")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_minutes_not_two_digits():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("08:5", "09:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_hours_too_many_digits():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("023:00", "00:00")
    assert "Invalid time" in str(exc.value)

def test_invalid_time_12_hour_exceeds_limits():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("13:00 PM", "14:00")
    assert str(exc.value) == "Invalid time: '13:00 PM'"

def test_break_duration_exceeds_worked_time():
    with pytest.raises(Exception) as exc:
        calculate_work_hours("09:00", "09:30", "01:00")
    assert str(exc.value) == "Break duration exceeds time worked"