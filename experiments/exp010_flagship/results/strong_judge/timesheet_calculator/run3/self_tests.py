import pytest
from solution import calculate_worked_hours

# US-1: Compute the worked duration of a shift
def test_duration_reported_in_zero_padded_HH_MM():
    assert calculate_worked_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes

def test_duration_with_break_subtracted():
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:08"  # 16:20 - 08:42 - 00:30 = 7 hours 8 minutes

def test_duration_with_zero_break_equals_no_break():
    assert calculate_worked_hours("08:42", "16:20", "00:00") == "07:38"  # 16:20 - 08:42 = 7 hours 38 minutes, no break

def test_identical_start_and_end_times():
    assert calculate_worked_hours("09:00", "09:00") == "00:00"  # No time worked

def test_full_day_shift():
    assert calculate_worked_hours("00:00", "23:59") == "23:59"  # 23:59 - 00:00 = 23 hours 59 minutes

# US-2: Handle overnight shifts
def test_shift_crossing_midnight():
    assert calculate_worked_hours("23:00", "01:00") == "02:00"  # 01:00 - 23:00 = 2 hours

def test_overnight_shift_with_break():
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"  # 02:09 - 17:02 - 00:35 = 8 hours 32 minutes

# US-3: Accept flexible time notations
def test_compact_digit_notation():
    assert calculate_worked_hours("800", "1530") == "07:30"  # 15:30 - 08:00 = 7 hours 30 minutes

def test_mixed_colon_and_compact_notation():
    assert calculate_worked_hours("08:42", "1620", "00:30") == "07:08"  # 16:20 - 08:42 - 00:30 = 7 hours 8 minutes

def test_12_hour_notation():
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"  # 16:30 - 08:00 = 8 hours 30 minutes

def test_midnight_and_noon_notation():
    assert calculate_worked_hours("12:00 AM", "12:00 PM") == "12:00"  # 12:00 - 00:00 = 12 hours

def test_lowercase_am_pm():
    assert calculate_worked_hours("8:00 am", "4:30 pm") == "08:30"  # 16:30 - 08:00 = 8 hours 30 minutes

def test_mixed_12_and_24_hour_notation():
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"  # 17:00 - 08:00 = 9 hours

def test_break_in_12_hour_notation():
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"  # 23:00 - 06:00 - 13:00 = 4 hours

def test_compact_break_notation():
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"  # 16:20 - 08:42 - 00:30 = 7 hours 8 minutes

# US-4: Reject invalid times and breaks
def test_invalid_hour_too_high():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("24:00", "01:00")

def test_invalid_hour_too_high_boundary():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("25:00", "01:00")

def test_invalid_minute_too_high():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("00:60", "01:00")

def test_invalid_minute_too_high_boundary():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("00:75", "01:00")

def test_non_numeric_time_entry():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("abc", "01:00")

def test_invalid_minutes_format():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("8:5", "01:00")

def test_invalid_hours_format():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("023:00", "01:00")

def test_invalid_hour_in_12_hour_notation():
    with pytest.raises(Exception, match=r"^Invalid time: '13:00 PM'$"):
        calculate_worked_hours("13:00 PM", "01:00")

def test_break_duration_exceeds_time_worked():
    with pytest.raises(Exception, match=r"^Break duration exceeds time worked$"):
        calculate_worked_hours("08:00", "09:00", "01:01")

def test_invalid_break_format():
    with pytest.raises(Exception, match="Invalid time"):
        calculate_worked_hours("08:00", "09:00", "00:60")