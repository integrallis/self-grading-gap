import pytest
from solution import last_sunday_of_year, last_sunday_of_month

# US-1: List a year's last Sundays
def test_last_sundays_of_2013():
    # Worked example: 2013 yields 2013-01-27, 2013-02-24, 2013-03-31, 2013-04-28,
    # 2013-05-26, 2013-06-30, 2013-07-28, 2013-08-25, 2013-09-29, 2013-10-27,
    # 2013-11-24, 2013-12-29.
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28",
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25",
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert last_sunday_of_year(2013) == expected

def test_last_sundays_of_2000():
    # December 31 falls on a Sunday, it is December's entry.
    expected = [
        "2000-01-30", "2000-02-27", "2000-03-26", "2000-04-30",
        "2000-05-28", "2000-06-25", "2000-07-30", "2000-08-27",
        "2000-09-24", "2000-10-29", "2000-11-26", "2000-12-31"
    ]
    assert last_sunday_of_year(2000) == expected

# US-2: Honor leap-year rules
def test_last_sundays_of_2032():
    # Leap year with February 29 on a Sunday.
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25",
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29",
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert last_sunday_of_year(2032) == expected

def test_last_sundays_of_2024():
    # Leap year with February 29 on a weekday; February's entry is the Sunday before it.
    expected = [
        "2024-01-28", "2024-02-25", "2024-03-31", "2024-04-28",
        "2024-05-26", "2024-06-30", "2024-07-28", "2024-08-25",
        "2024-09-29", "2024-10-27", "2024-11-24", "2024-12-29"
    ]
    assert last_sunday_of_year(2024) == expected

def test_last_sundays_of_2100():
    # Century year not divisible by 400 is not a leap year; February ends on the 28th.
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25",
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29",
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert last_sunday_of_year(2100) == expected

# US-3: Look up a single month
def test_last_sunday_of_january_2013():
    # January 2013 gives January 27.
    assert last_sunday_of_month(2013, 1) == "2013-01-27"

def test_last_sunday_of_march_2013():
    # March 2013 gives March 31, the month's final day.
    assert last_sunday_of_month(2013, 3) == "2013-03-31"

def test_last_sunday_of_february_2024():
    # February 2024 gives February 25, the Sunday before the leap day.
    assert last_sunday_of_month(2024, 2) == "2024-02-25"

def test_last_sunday_of_december_2000():
    # December 2000 gives December 31, which is a Sunday.
    assert last_sunday_of_month(2000, 12) == "2000-12-31"

def test_invalid_month_0():
    # Month outside 1 through 12 is refused as an error.
    with pytest.raises(Exception) as excinfo:
        last_sunday_of_month(2023, 0)
    assert str(excinfo.value) == "month must be in 1..12"

def test_invalid_month_13():
    # Month outside 1 through 12 is refused as an error.
    with pytest.raises(Exception) as excinfo:
        last_sunday_of_month(2023, 13)
    assert str(excinfo.value) == "month must be in 1..12"