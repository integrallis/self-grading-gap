from solution import calculate_worked_hours
import pytest

def test_compute_worked_duration():
    # AC-1.1
    assert calculate_worked_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes
    assert calculate_worked_hours("09:05", "09:13") == "00:08"  # 09:13 - 09:05 = 0 hours 8 minutes
    # AC-1.2
    assert calculate_worked_hours("08:42", "16:20", "00:30") == "07:08"  # (16:20 - 08:42) - 00:30 = 7 hours 8 minutes
    # AC-1.3
    assert calculate_worked_hours("08:42", "16:20") == "07:38"  # Same as AC-1.2 without break
    # AC-1.4
    assert calculate_worked_hours("10:00", "10:00") == "00:00"  # No time worked
    # AC-1.5
    assert calculate_worked_hours("00:00", "23:59") == "23:59"  # Full day worked

def test_handle_overnight_shifts():
    # AC-2.1
    assert calculate_worked_hours("23:00", "01:00") == "02:00"  # 1:00 AM is 2 hours after 11:00 PM
    # AC-2.2
    assert calculate_worked_hours("17:02", "02:09", "00:35") == "08:32"  # (02:09 - 17:02) - 00:35 = 8 hours 32 minutes

def test_flexible_time_notations():
    # AC-3.1
    assert calculate_worked_hours("800", "1530") == "07:30"  # 08:00 to 15:30 is 7 hours 30 minutes
    assert calculate_worked_hours("0842", "1620", "0030") == "07:08"  # Same as AC-1.2
    # AC-3.2
    assert calculate_worked_hours("08:00", "1530") == "07:30"  # Mixed notations
    # AC-3.3
    assert calculate_worked_hours("8:00 AM", "4:30 PM") == "08:30"  # 08:00 to 16:30
    # AC-3.4
    assert calculate_worked_hours("12:00 AM", "01:00") == "01:00"  # Midnight to 1:00 AM
    assert calculate_worked_hours("12:00 PM", "13:00") == "01:00"  # Noon to 1:00 PM
    # AC-3.5
    assert calculate_worked_hours("12:00 am", "12:00 pm") == "12:00"  # Lowercase
    # AC-3.6
    assert calculate_worked_hours("8:00 AM", "17:00") == "09:00"  # Mixed formats
    # AC-3.7
    assert calculate_worked_hours("06:00", "23:00", "1:00 PM") == "04:00"  # (23:00 - 06:00) - 13:00 = 4 hours

def test_reject_invalid_times_and_breaks():
    # AC-4.1
    with pytest.raises(Exception) as e:
        calculate_worked_hours("24:00", "01:00")
    assert "Invalid time" in str(e.value)

    with pytest.raises(Exception) as e:
        calculate_worked_hours("25:00", "01:00")
    assert "Invalid time" in str(e.value)
    
    # AC-4.2
    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "08:60")
    assert "Invalid time" in str(e.value)

    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "08:75")
    assert "Invalid time" in str(e.value)
    
    # AC-4.3
    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "invalid")
    assert "Invalid time" in str(e.value)
    
    # AC-4.4
    with pytest.raises(Exception) as e:
        calculate_worked_hours("8:5", "09:00")
    assert "Invalid time" in str(e.value)
    
    # AC-4.5
    with pytest.raises(Exception) as e:
        calculate_worked_hours("023:00", "01:00")
    assert "Invalid time" in str(e.value)
    
    # AC-4.6
    with pytest.raises(Exception) as e:
        calculate_worked_hours("13:00 PM", "01:00")
    assert str(e.value) == "Invalid time: '13:00 PM'"
    
    # AC-4.7
    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "10:00", "02:01")
    assert str(e.value) == "Break duration exceeds time worked"
    
    # Test invalid break inputs
    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "10:00", "invalid")
    assert "Invalid time" in str(e.value)
    
    with pytest.raises(Exception) as e:
        calculate_worked_hours("08:00", "10:00", "10:60")
    assert "Invalid time" in str(e.value)