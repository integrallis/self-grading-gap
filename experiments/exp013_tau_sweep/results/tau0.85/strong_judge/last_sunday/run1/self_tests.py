import pytest
from solution import get_last_sundays, get_last_sunday_of_month

# US-1: List a year's last Sundays
def test_get_last_sundays_2013():
    # Expecting last Sundays for each month in 2013
    # January: 27, February: 24, March: 31, April: 28, May: 26, June: 30, 
    # July: 28, August: 25, September: 29, October: 27, November: 24, December: 29
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28", 
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25", 
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert get_last_sundays(2013) == expected

def test_get_last_sundays_2000():
    # December 31, 2000 is a Sunday; it should be the last Sunday of December.
    # Last Sundays: 2000-01-30, 2000-02-27, 2000-03-26, 2000-04-30, 
    # 2000-05-28, 2000-06-25, 2000-07-30, 2000-08-27, 2000-09-24, 
    # 2000-10-29, 2000-11-26, 2000-12-31
    expected = [
        "2000-01-30", "2000-02-27", "2000-03-26", "2000-04-30", 
        "2000-05-28", "2000-06-25", "2000-07-30", "2000-08-27", 
        "2000-09-24", "2000-10-29", "2000-11-26", "2000-12-31"
    ]
    assert get_last_sundays(2000) == expected

def test_get_last_sundays_2032():
    # In 2032, February 29 is a Sunday.
    # Last Sundays: 2032-01-25, 2032-02-29, 2032-03-28, 2032-04-25, 
    # 2032-05-30, 2032-06-27, 2032-07-25, 2032-08-29, 
    # 2032-09-26, 2032-10-31, 2032-11-28, 2032-12-26
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25", 
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29", 
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert get_last_sundays(2032) == expected

def test_get_last_sundays_2024():
    # In 2024, February 29 is a Thursday, so the last Sunday is February 25.
    # Last Sundays: 2024-01-28, 2024-02-25, 2024-03-31, 2024-04-28, 
    # 2024-05-26, 2024-06-30, 2024-07-28, 2024-08-25, 
    # 2024-09-29, 2024-10-27, 2024-11-24, 2024-12-29
    expected = [
        "2024-01-28", "2024-02-25", "2024-03-31", "2024-04-28", 
        "2024-05-26", "2024-06-30", "2024-07-28", "2024-08-25", 
        "2024-09-29", "2024-10-27", "2024-11-24", "2024-12-29"
    ]
    assert get_last_sundays(2024) == expected

def test_get_last_sundays_2100():
    # 2100 is not a leap year; February ends on the 28th.
    # Last Sundays: 2100-01-31, 2100-02-28, 2100-03-28, 2100-04-25, 
    # 2100-05-30, 2100-06-27, 2100-07-25, 2100-08-29, 
    # 2100-09-26, 2100-10-31, 2100-11-28, 2100-12-26
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25", 
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29", 
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert get_last_sundays(2100) == expected

# US-3: Look up a single month
def test_get_last_sunday_of_month_january_2013():
    # Last Sunday of January 2013 is 27
    expected = "2013-01-27"
    assert get_last_sunday_of_month(2013, 1) == expected

def test_get_last_sunday_of_month_march_2013():
    # Last Sunday of March 2013 is 31
    expected = "2013-03-31"
    assert get_last_sunday_of_month(2013, 3) == expected

def test_get_last_sunday_of_month_february_2024():
    # Last Sunday of February 2024 is 25
    expected = "2024-02-25"
    assert get_last_sunday_of_month(2024, 2) == expected

def test_get_last_sunday_of_month_invalid_month():
    # Month 13 is invalid.
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        get_last_sunday_of_month(2023, 13)

def test_get_last_sunday_of_month_invalid_negative_month():
    # Month 0 is invalid.
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        get_last_sunday_of_month(2023, 0)