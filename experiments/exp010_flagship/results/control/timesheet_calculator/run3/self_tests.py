from solution import calculate_work_hours

def test_duration_between_clock_in_and_clock_out():
    # AC-1.1
    assert calculate_work_hours("07:02", "16:22") == "09:20"  # 16:22 - 07:02 = 9 hours 20 minutes
    # AC-1.2
    assert calculate_work_hours("08:42", "16:20", "00:30") == "07:08"  # 16:20 - 08:42 - 00:30 = 7 hours 8 minutes
    # AC-1.3
    assert calculate_work_hours("08:42", "16:20", "00:00") == "07:08"  # Same result as above, no break
    # AC-1.4
    assert calculate_work_hours("12:00", "12:00") == "00:00"  # Identical times mean no time worked
    # AC-1.5
    assert calculate_work_hours("00:00", "23:59") == "23:59"  # Full duration from 00:00 to 23:59

def test_overnight_shifts():
    # AC-2.1
    assert calculate_work_hours("23:00", "01:00") == "02:00"  # Shift crosses midnight
    # AC-2.2
    assert calculate_work_hours("17:02", "02:09", "00:35") == "08:32"  # Overnight shift with break

def test_flexible_time_notations():
    # AC-3.1
    assert calculate_work_hours("800", "1530") == "07:30"  # Compact digits
    assert calculate_work_hours("0842", "1620", "0030") == "07:08"  # Mixed colon and compact digits
    # AC-3.2
    assert calculate_work_hours("07:02", "1622") == "09:20"  # Mixed notations
    # AC-3.3
    assert calculate_work_hours("8:00 AM", "4:30 PM") == "08:30"  # 12-hour format
    # AC-3.4
    assert calculate_work_hours("12:00 AM", "12:00 PM") == "12:00"  # Midnight to noon
    # AC-3.5
    assert calculate_work_hours("8:00 am", "4:30 pm") == "08:30"  # Lowercase am/pm
    # AC-3.6
    assert calculate_work_hours("8:00 AM", "17:00") == "09:00"  # Mixed 12-hour and 24-hour
    # AC-3.7
    assert calculate_work_hours("06:00", "23:00", "1:00 PM") == "04:00"  # Break in 12-hour notation

def test_reject_invalid_times_and_breaks():
    # AC-4.1
    try:
        calculate_work_hours("24:00", "01:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    try:
        calculate_work_hours("25:00", "01:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    # AC-4.2
    try:
        calculate_work_hours("08:60", "09:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    try:
        calculate_work_hours("08:75", "09:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    # AC-4.3
    try:
        calculate_work_hours("08:00", "not_a_time")
    except ValueError as e:
        assert str(e) == "Invalid time"

    # AC-4.4
    try:
        calculate_work_hours("8:5", "09:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    # AC-4.5
    try:
        calculate_work_hours("023:00", "01:00")
    except ValueError as e:
        assert str(e) == "Invalid time"

    # AC-4.6
    try:
        calculate_work_hours("13:00 PM", "01:00")
    except ValueError as e:
        assert str(e) == "Invalid time: '13:00 PM'"

    # AC-4.7
    try:
        calculate_work_hours("06:00", "07:00", "01:00")
    except ValueError as e:
        assert str(e) == "Break duration exceeds time worked"