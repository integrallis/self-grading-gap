import pytest
from solution import *

# US-1: Compute the worked duration of a shift
def test_duration_in_zero_padded_format():
    assert calculate_worked_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes
    assert calculate_worked_hours("09:05", "09:13") == "00:08"  # 09:13 - 09:05 = 8 minutes

def test_duration_with_break():
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:38"  # (16:20 - 08:42) - 30 minutes = 7 hours 38 minutes

def test_duration_with_zero_break():
    assert calculate_worked_hours("08:42", "16:20", "00:00") == calculate_worked_hours("08:42", "16:20")  # Same as above, break of 00:00

def test_identical_start_and_end_times():
    assert calculate_worked_hours("12:00", "12:00") == "00:00"  # No time worked

def test_full_day_shift():
    assert calculate_worked_hours("00:00", "23:59") == "23:59"  # Full day shift

# US-2: Handle overnight shifts
def test_overnight_shift():
    assert calculate_worked_hours("23:00", "01:00") == "02:00"  # 01:00 next day - 23:00 = 2 hours

def test_overnight_shift_with_break():
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"  # (02:09 - 17:02) - 35 minutes = 8 hours 32 minutes

# US-3: Accept flexible time notations
def test_time_notation_without_colon():
    assert calculate_worked_hours("800", "1530") == "07:30"  # 8:00 - 15:30 = 7 hours 30 minutes
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"  # (16:20 - 08:42) - 30 minutes = 7 hours 8 minutes

def test_mixed_time_notation():
    assert calculate_worked_hours("800", "15:30") == "07:30"  # 08:00 - 15:30 = 7 hours 30 minutes

def test_twelve_hour_notation():
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"  # 08:00 - 16:30 = 8 hours 30 minutes
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"  # 08:00 - 17:00 = 9 hours
    assert calculate_worked_hours("12:00 AM", "12:00 PM") == "12:00"  # Midnight to noon is 12 hours
    assert calculate_worked_hours("12:00 PM", "1:00 PM") == "01:00"  # Noon to 1 PM is 1 hour
    assert calculate_worked_hours("1:00 PM", "12:00 AM") == "11:00"  # 1 PM to midnight is 11 hours
    assert calculate_worked_hours("11:00 PM", "12:59 AM") == "01:59"  # 11 PM to 1 AM is 1 hour 59 minutes
    assert calculate_worked_hours("8:00 am", "4:30 pm") == "08:30"  # 08:00 - 16:30 = 8 hours 30 minutes

# US-4: Reject invalid times and breaks
def test_invalid_times():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("24:00", "00:00")  # Hour 24 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("25:00", "00:00")  # Hour 25 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("12:60", "13:00")  # Minute 60 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("12:00 PM", "13:00 PM")  # Hour 13 in PM is invalid
    with pytest.raises(Exception, match="Invalid time: '13:00 PM'"):
        calculate_worked_hours("13:00 PM", "14:00")  # Hour 13 in PM is invalid
    
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("8:5", "9:00")  # Invalid minutes format
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("023:00", "00:00")  # Invalid hours format
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("12:00 PM", "14:00 PM")  # Hour 13 in PM is invalid

def test_break_exceeds_time_worked():
    with pytest.raises(Exception, match="Break duration exceeds time worked"):
        calculate_worked_hours("08:00", "09:00", "01:01")  # Break longer than worked time

def test_invalid_minute_75():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("12:75", "13:00")  # Minute 75 is invalid

def test_non_numeric_time_entry():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("abc", "09:00")  # Non-numeric time entry

def test_twelve_hour_break():
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"  # (23:00 - 06:00) - 1:00 (13:00) = 4 hours