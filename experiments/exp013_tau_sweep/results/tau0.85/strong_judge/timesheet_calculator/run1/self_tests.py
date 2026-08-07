import pytest
from solution import calculate_work_hours

def test_compute_worked_duration():
    # AC-1.1: 07:02 to 16:22 is 09:20
    assert calculate_work_hours("07:02", "16:22") == "09:20"
    # AC-1.1: 09:05 to 09:13 is 00:08
    assert calculate_work_hours("09:05", "09:13") == "00:08"
    # AC-1.2: 08:42 to 16:20 with a 00:30 break is 07:08
    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"
    # AC-1.3: A break of 00:00 gives same result as no break
    assert calculate_work_hours("08:42", "16:20", "00:00") == "07:08"
    # AC-1.4: Identical start and end times mean no time worked
    assert calculate_work_hours("09:00", "09:00") == "00:00"
    # AC-1.5: A shift from 00:00 to 23:59 is 23:59
    assert calculate_work_hours("00:00", "23:59") == "23:59"

def test_handle_overnight_shifts():
    # AC-2.1: 23:00 to 01:00 is 02:00
    assert calculate_work_hours("23:00", "01:00") == "02:00"
    # AC-2.2: 17:02 to 02:09 with a 00:35 break is 08:32
    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"

def test_flexible_time_notations():
    # AC-3.1: "800" to "1530" is 07:30
    assert calculate_work_hours("800", "1530") == "07:30"
    # AC-3.2: Mixed colon and colon-free notations
    assert calculate_work_hours("08:42", "1620") == "07:38"  # Mixed notations
    # AC-3.3: 8:00 AM to 4:30 PM is 08:30
    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"
    # AC-3.4: 12:00 AM means midnight
    assert calculate_work_hours("12:00 AM", "01:00") == "01:00"  # Midnight to 1 AM
    assert calculate_work_hours("12:00 PM", "13:00") == "01:00"  # Noon to 1 PM
    # AC-3.5: Lowercase am/pm markers are accepted
    assert calculate_work_hours("8:00 am", "4:30 pm") == "08:30"
    # AC-3.6: Mixed 12-hour and 24-hour notations
    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"
    # AC-3.7: A break of 1:00 PM means thirteen hours
    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"

def test_reject_invalid_times_and_breaks():
    # AC-4.1: Hour 24 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("24:00", "01:00")
    # AC-4.1: Hour 25 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("25:00", "01:00")
    # AC-4.2: Minute 60 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("08:60", "09:00")
    # AC-4.2: Minute 75 is invalid
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("08:75", "09:00")
    # AC-4.3: Non-numeric time entry is rejected
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("abc", "09:00")
    # AC-4.4: Minutes field must be exactly two digits
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("8:5", "09:00")
    # AC-4.5: Hours field is at most two digits
    with pytest.raises(Exception, match="Invalid time"):
        calculate_work_hours("023:00", "09:00")
    # AC-4.6: In 12-hour notation, hour may not exceed 12
    with pytest.raises(Exception) as exc:
        calculate_work_hours("13:00 PM", "01:00 PM")
    assert str(exc.value) == "Invalid time: '13:00 PM'"
    # AC-4.7: Break longer than elapsed shift
    with pytest.raises(Exception) as exc:
        calculate_work_hours("08:00", "09:00", "01:01")
    assert str(exc.value) == "Break duration exceeds time worked"