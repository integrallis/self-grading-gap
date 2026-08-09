import pytest
from solution import *

def test_worked_duration_basic():
    # 07:02 to 16:22 is 09:20
    assert calculate_worked_hours("07:02", "16:22") == "09:20"

def test_worked_duration_with_break():
    # 08:42 to 16:20 with a 00:30 break is 07:08
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:08"

def test_worked_duration_with_zero_break():
    # 08:42 to 16:20 with a 00:00 break is 07:08
    assert calculate_worked_hours("08:42", "16:20", "00:00") == "07:08"

def test_worked_duration_identical_times():
    # Identical start and end times mean no time worked: 00:00
    assert calculate_worked_hours("12:00", "12:00") == "00:00"

def test_worked_duration_full_day():
    # A shift from 00:00 to 23:59 is 23:59
    assert calculate_worked_hours("00:00", "23:59") == "23:59"

def test_overnight_shift():
    # 23:00 to 01:00 is 02:00
    assert calculate_worked_hours("23:00", "01:00") == "02:00"

def test_overnight_shift_with_break():
    # 17:02 to 02:09 with a 00:35 break is 08:32
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"

def test_no_colon_time_format():
    # "800" to "1530" is 07:30
    assert calculate_worked_hours("800", "1530") == "07:30"

def test_mixed_time_formats():
    # "0842" to "1620" with "0030" break matches the colon form's 07:08
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"

def test_12_hour_time_format():
    # 8:00 AM to 4:30 PM is 08:30
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"

def test_midnight_noon_times():
    # 12:00 AM means midnight and 12:00 PM means noon
    assert calculate_worked_hours("12:00 AM", "12:00 PM") == "12:00"

def test_lowercase_am_pm():
    # 8:00 am to 5:00 pm is 09:00
    assert calculate_worked_hours("8:00 am", "5:00 pm") == "09:00"

def test_mixed_12_and_24_hour_formats():
    # 8:00 AM to 17:00 is 09:00
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"

def test_12_hour_break_time():
    # A break of 1:00 PM means thirteen hours
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"

def test_invalid_time_hour_out_of_bounds():
    # Hour 24 is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("24:00", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_hour_too_high():
    # Hour 25 is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("25:00", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_minute_out_of_bounds():
    # Minute 60 is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("00:60", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_minute_too_high():
    # Minute 75 is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("00:75", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_non_numeric():
    # Non-numeric time entry is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("abc", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_minute_format():
    # Minute format like "8:5" is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("08:5", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_hour_format():
    # Hour format like "023:00" is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("023:00", "01:00")
    assert str(exc.value) == "Invalid time"

def test_invalid_time_12_hour_format():
    # "13:00 PM" should be rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("13:00 PM", "01:00")
    assert str(exc.value) == "Invalid time: '13:00 PM'"

def test_break_exceeds_time_worked():
    # Break longer than the shift time is rejected
    with pytest.raises(Exception) as exc:
        calculate_worked_hours("08:00", "09:00", "01:01")
    assert str(exc.value) == "Break duration exceeds time worked"

def test_under_one_hour_duration():
    # 09:05 to 09:13 is 00:08
    assert calculate_worked_hours("09:05", "09:13") == "00:08"