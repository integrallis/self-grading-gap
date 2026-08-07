import pytest
from solution import calculate_work_hours

def test_calculate_work_hours_standard_times():
    # AC-1.1
    assert calculate_work_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes
    # AC-1.2
    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"  # 16:20 - 08:42 - 30 min = 7 hours 8 minutes
    # AC-1.3
    assert calculate_work_hours("08:42", "16:20", "00:00") == "07:38"  # Same as above without break
    assert calculate_work_hours("08:42", "16:20") == "07:38"  # Same as above without break
    # AC-1.4
    assert calculate_work_hours("09:00", "09:00") == "00:00"  # No time worked
    # AC-1.5
    assert calculate_work_hours("00:00", "23:59") == "23:59"  # Full day worked

def test_calculate_work_hours_overnight_shifts():
    # AC-2.1
    assert calculate_work_hours("23:00", "01:00") == "02:00"  # 1 AM next day is 2 hours
    # AC-2.2
    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"  # Overnight with break

def test_calculate_work_hours_flexible_time_notations():
    # AC-3.1
    assert calculate_work_hours("800", "1530") == "07:30"  # 8:00 to 15:30
    assert calculate_work_hours("0842", "1620", "0030") == "07:08"  # 8:42 to 16:20 with a 30 min break
    # AC-3.2
    assert calculate_work_hours("800", "16:30") == "08:30"  # Mixed notation
    # AC-3.3
    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"  # 12-hour format
    # AC-3.4
    assert calculate_work_hours("12:00 AM", "01:00") == "01:00"  # Midnight to 1 AM
    assert calculate_work_hours("12:00 PM", "13:00") == "01:00"  # Noon to 1 PM
    # AC-3.5
    assert calculate_work_hours("12:00 am", "12:00 pm") == "12:00"  # Case insensitive
    # AC-3.6
    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"  # Mixed 12 and 24-hour
    # AC-3.7
    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"  # Break in 12-hour notation

def test_calculate_work_hours_invalid_times():
    # AC-4.1
    with pytest.raises(Exception):
        calculate_work_hours("24:00", "01:00")

    with pytest.raises(Exception):
        calculate_work_hours("25:00", "01:00")

    # AC-4.2
    with pytest.raises(Exception):
        calculate_work_hours("08:60", "09:00")

    with pytest.raises(Exception):
        calculate_work_hours("08:75", "09:00")

    # AC-4.3
    with pytest.raises(Exception):
        calculate_work_hours("08:xx", "09:00")

    # AC-4.4
    with pytest.raises(Exception):
        calculate_work_hours("8:5", "09:00")

    # AC-4.5
    with pytest.raises(Exception):
        calculate_work_hours("023:00", "09:00")

    # AC-4.6
    with pytest.raises(Exception) as e:
        calculate_work_hours("13:00 PM", "14:00")
    assert str(e.value) == "Invalid time: '13:00 PM'"

    # AC-4.7
    with pytest.raises(Exception) as e:
        calculate_work_hours("10:00", "12:00", "03:00")
    assert str(e.value) == "Break duration exceeds time worked"