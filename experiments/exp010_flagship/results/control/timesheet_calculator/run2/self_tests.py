import pytest
from solution import calculate_worked_hours

def test_calculate_worked_hours_standard_times():
    # AC-1.1: 07:02 to 16:22 is 09:20
    assert calculate_worked_hours("07:02", "16:22") == "09:20"
    
    # AC-1.2: 08:42 to 16:20 with a 00:30 break is 07:08
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:08"
    
    # AC-1.3: A break of 00:00 gives the same result as giving no break at all
    assert calculate_worked_hours("08:42", "16:20", "00:00") == "07:08"
    
    # AC-1.4: Identical start and end times mean no time worked: 00:00
    assert calculate_worked_hours("09:00", "09:00") == "00:00"
    
    # AC-1.5: A shift from 00:00 to 23:59 is 23:59
    assert calculate_worked_hours("00:00", "23:59") == "23:59"

def test_calculate_worked_hours_overnight_shifts():
    # AC-2.1: 23:00 to 01:00 is 02:00
    assert calculate_worked_hours("23:00", "01:00") == "02:00"
    
    # AC-2.2: 17:02 to 02:09 with a 00:35 break is 08:32
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"

def test_calculate_worked_hours_flexible_time_notations():
    # AC-3.1: "800" to "1530" is 07:30
    assert calculate_worked_hours("800", "1530") == "07:30"
    
    # AC-3.2: Mixed colon and colon-free notations
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"
    
    # AC-3.3: 8:00 AM to 4:30 PM is 08:30
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"
    
    # AC-3.4: 12:00 AM means midnight
    assert calculate_worked_hours("12:00 AM", "1:00 AM") == "01:00"
    
    # AC-3.5: Lowercase am/pm markers are accepted
    assert calculate_worked_hours("8:00 am", "4:30 pm") == "08:30"
    
    # AC-3.6: Mixed 12-hour and 24-hour notations
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"
    
    # AC-3.7: 06:00 to 23:00 shift minus a break of 1:00 PM
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"

def test_calculate_worked_hours_invalid_times_and_breaks():
    # AC-4.1: Reject hour 24
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("24:00", "01:00")
    
    # AC-4.2: Reject minute 60
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("08:60", "09:00")
    
    # AC-4.3: Reject non-numeric time entry
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("abc", "10:00")
    
    # AC-4.4: Reject invalid minute format
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("8:5", "09:00")
    
    # AC-4.5: Reject invalid hour format
    with pytest.raises(ValueError, match="Invalid time"):
        calculate_worked_hours("023:00", "01:00")
    
    # AC-4.6: Reject hour exceeding 12 in 12-hour notation
    with pytest.raises(ValueError, match="Invalid time: '13:00 PM'"):
        calculate_worked_hours("13:00 PM", "01:00 PM")
    
    # AC-4.7: Reject break longer than the elapsed shift
    with pytest.raises(ValueError, match="Break duration exceeds time worked"):
        calculate_worked_hours("08:00", "09:00", "01:00")