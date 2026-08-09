import pytest
from solution import last_sundays_in_year, last_sunday_of_month
from datetime import date, timedelta

# US-1: List a year's last Sundays
def test_last_sundays_in_year_2013():
    # 2013 last Sundays: 
    # January: 27, February: 24, March: 31, April: 28, May: 26, June: 30,
    # July: 28, August: 25, September: 29, October: 27, November: 24, December: 29
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28", 
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25", 
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert last_sundays_in_year(2013) == expected

def test_last_sundays_in_year_2000():
    # 2000 last Sundays: 
    # January: 30, February: 27, March: 26, April: 30, May: 28, June: 25,
    # July: 30, August: 27, September: 24, October: 29, November: 26, December: 31
    expected = [
        "2000-01-30", "2000-02-27", "2000-03-26", "2000-04-30", 
        "2000-05-28", "2000-06-25", "2000-07-30", "2000-08-27", 
        "2000-09-24", "2000-10-29", "2000-11-26", "2000-12-31"
    ]
    assert last_sundays_in_year(2000) == expected

def test_last_sundays_in_year_2032():
    # 2032 last Sundays: 
    # January: 25, February: 29, March: 28, April: 25, May: 30, June: 27,
    # July: 25, August: 29, September: 26, October: 31, November: 28, December: 26
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25", 
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29", 
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert last_sundays_in_year(2032) == expected

def test_last_sundays_in_year_2024():
    # 2024 last Sundays: 
    # January: 28, February: 25, March: 31, April: 28, May: 26, June: 30,
    # July: 28, August: 25, September: 29, October: 27, November: 24, December: 29
    expected = [
        "2024-01-28", "2024-02-25", "2024-03-31", "2024-04-28", 
        "2024-05-26", "2024-06-30", "2024-07-28", "2024-08-25", 
        "2024-09-29", "2024-10-27", "2024-11-24", "2024-12-29"
    ]
    assert last_sundays_in_year(2024) == expected

def test_last_sundays_in_year_2100():
    # 2100 last Sundays: 
    # January: 31, February: 28, March: 28, April: 25, May: 30, June: 27,
    # July: 25, August: 29, September: 26, October: 31, November: 28, December: 26
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25", 
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29", 
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert last_sundays_in_year(2100) == expected

# US-3: Look up a single month
def test_last_sunday_of_month_january_2013():
    # January 2013 last Sunday: January 27
    expected = "2013-01-27"
    assert last_sunday_of_month(2013, 1) == expected

def test_last_sunday_of_month_march_2013():
    # March 2013 last Sunday: March 31
    expected = "2013-03-31"
    assert last_sunday_of_month(2013, 3) == expected

def test_last_sunday_of_month_february_2024():
    # February 2024 last Sunday: February 25
    expected = "2024-02-25"
    assert last_sunday_of_month(2024, 2) == expected

def test_last_sunday_of_month_february_2032():
    # February 2032 last Sunday: February 29
    expected = "2032-02-29"
    assert last_sunday_of_month(2032, 2) == expected

def test_last_sunday_of_month_invalid_month():
    # Invalid month should raise an error with the specified message
    with pytest.raises(Exception, match=r"\Amonth must be in 1\.\.12\Z"):
        last_sunday_of_month(2023, 13)

def test_last_sunday_of_month_invalid_month_below():
    # Invalid month should raise an error with the specified message
    with pytest.raises(Exception, match=r"\Amonth must be in 1\.\.12\Z"):
        last_sunday_of_month(2023, 0)

def test_last_sunday_of_month_invalid_month_negative():
    # Invalid month should raise an error with the specified message
    with pytest.raises(Exception, match=r"\Amonth must be in 1\.\.12\Z"):
        last_sunday_of_month(2023, -1)

def test_last_sunday_of_month_invalid_month_above():
    # Invalid month should raise an error with the specified message
    with pytest.raises(Exception, match=r"\Amonth must be in 1\.\.12\Z"):
        last_sunday_of_month(2023, 14)

# General algorithm tests for last Sundays
def test_last_sundays_in_year_general():
    for year in range(2001, 2101):
        expected = []
        for month in range(1, 13):
            last_day = date(year, month + 1, 1) - timedelta(days=1) if month < 12 else date(year, month, 31)
            last_sunday = last_day - timedelta(days=(last_day.weekday() + 1) % 7)
            expected.append(last_sunday.isoformat())
        assert last_sundays_in_year(year) == expected