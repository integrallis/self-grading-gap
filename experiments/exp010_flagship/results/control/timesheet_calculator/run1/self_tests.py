import pytest
from solution import calculate_worked_hours

# US-1: Compute the worked duration of a shift
def test_duration_example_1():
    assert calculate_worked_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes

def test_duration_with_break():
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:08"  # (16:20 - 08:42) - 00:30 = 7 hours 8 minutes

def test_duration_no_break():
    assert calculate_worked_hours("08:42", "16:20", "00:00") == "07:08"  # Same as previous case

def test_duration_identical_times():
    assert calculate_worked_hours("09:00", "09:00") == "00:00"  # Same start and end time means 0 worked hours

def test_duration_full_day():
    assert calculate_worked_hours("00:00", "23:59") == "23:59"  # Full shift from start to end of day

# US-2: Handle overnight shifts
def test_overnight_shift():
    assert calculate_worked_hours("23:00", "01:00") == "02:00"  # 01:00 is next day, so 2 hours worked

def test_overnight_shift_with_break():
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"  # (02:09 - 17:02) - 00:35 = 8 hours 32 minutes

# US-3: Accept flexible time notations
def test_compact_time_notation():
    assert calculate_worked_hours("800", "1530") == "07:30"  # 15:30 - 08:00 = 7 hours 30 minutes

def test_mixed_time_notations():
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"  # Same as previous break calculation

def test_12_hour_notation():
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"  # 16:30 - 08:00 = 8 hours 30 minutes

def test_midnight_and_noon():
    assert calculate_worked_hours("12:00 AM", "12:00 PM") == "12:00"  # 12 hours from midnight to noon

def test_lowercase_am_pm():
    assert calculate_worked_hours("8:00 am", "4:30 pm") == "08:30"  # Same as previous test

def test_mixed_12_and_24_hour_notation():
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"  # 17:00 - 08:00 = 9 hours

def test_break_in_12_hour_notation():
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"  # (23:00 - 06:00) - 13:00 = 4 hours

# US-4: Reject invalid times and breaks
def test_invalid_hour_24():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("24:00", "01:00")

def test_invalid_hour_25():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("25:00", "01:00")

def test_invalid_minute_60():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("00:60", "01:00")

def test_invalid_minute_75():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("00:75", "01:00")

def test_non_numeric_time():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("abc", "01:00")

def test_invalid_minute_format():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("8:5", "01:00")

def test_invalid_hour_format():
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("023:00", "01:00")

def test_invalid_hour_12():
    with pytest.raises(ValueError, match="Invalid time: '13:00 PM'"):
        calculate_worked_hours("13:00 PM", "01:00")

def test_break_exceeds_worked_time():
    with pytest.raises(ValueError, match="Break duration exceeds time worked"):
        calculate_worked_hours("08:00", "09:00", "01:00")  # 1 hour break exceeds 1 hour worked