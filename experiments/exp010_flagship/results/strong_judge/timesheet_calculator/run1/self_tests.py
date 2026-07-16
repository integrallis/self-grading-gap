import pytest
from solution import calculate_work_hours

def test_work_duration_regular_times():
    # 07:02 to 16:22 is 09:20
    assert calculate_work_hours("07:02", "16:22") == "09:20"
    # 09:05 to 09:13 is 00:08
    assert calculate_work_hours("09:05", "09:13") == "00:08"

def test_work_duration_with_break():
    # 08:42 to 16:20 with a 00:30 break is 07:08
    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"

def test_work_duration_no_break():
    # 08:42 to 16:20 with a 00:00 break is 07:38
    assert calculate_work_hours("08:42", "16:20", "00:00") == "07:38"
    # Identical times means no time worked: 00:00
    assert calculate_work_hours("12:00", "12:00") == "00:00"
    # 00:00 to 23:59 is 23:59
    assert calculate_work_hours("00:00", "23:59") == "23:59"

def test_work_duration_overnight():
    # 23:00 to 01:00 is 02:00
    assert calculate_work_hours("23:00", "01:00") == "02:00"
    # 17:02 to 02:09 with a 00:35 break is 08:32
    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"

def test_work_duration_colon_free_notations():
    # "800" to "1530" is 07:30
    assert calculate_work_hours("800", "1530") == "07:30"
    # "0842" to "1620" with a "0030" break is 07:08
    assert calculate_work_hours("0842", "1620", "0030") == "07:08"

def test_work_duration_mixed_notations():
    # 8:00 AM to 4:30 PM is 08:30
    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"
    # 8:00 AM to 17:00 is 09:00
    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"
    # "08:00" to "1630" is 08:30
    assert calculate_work_hours("08:00", "1630") == "08:30"

def test_work_duration_invalid_times():
    # Invalid hour 24 should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("24:00", "01:00")
    # Invalid hour 25 should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("25:00", "01:00")
    # Invalid minute 60 should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("00:60", "01:00")
    # Invalid minute 75 should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("00:75", "01:00")
    # Invalid non-numeric time should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("abc", "01:00")
    # Invalid time format "8:5" should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("8:5", "01:00")
    # Invalid time format "023:00" should raise an error
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("023:00", "01:00")
    # Invalid hour in 12-hour notation "13:00 PM" should raise an error
    with pytest.raises(Exception, match="Invalid time: '13:00 PM'"):
        calculate_work_hours("13:00 PM", "01:00")

def test_break_exceeds_worked_time():
    # Break longer than the elapsed shift should raise an error
    with pytest.raises(Exception, match="Break duration exceeds time worked"):
        calculate_work_hours("08:00", "08:30", "01:00")

def test_midnight_and_noon():
    # 12:00 AM is midnight
    assert calculate_work_hours("12:00 AM", "12:00 PM") == "12:00"
    # 12:00 PM is noon
    assert calculate_work_hours("12:00 PM", "01:00 PM") == "01:00"

def test_lowercase_am_pm():
    # 8:00 am to 4:30 pm is 08:30
    assert calculate_work_hours("8:00 am", "4:30 pm") == "08:30"

def test_break_with_12_hour_notation():
    # 06:00 to 23:00 with a break of 1:00 PM is 04:00
    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"