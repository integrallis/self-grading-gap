# test_calendar_helper.py

import pytest
from solution import get_last_sundays, get_last_sunday_of_month

def test_get_last_sundays_for_year_2013():
    # Expected values computed from the specification:
    # January: 2013-01-27 (last Sunday of Jan 2013)
    # February: 2013-02-24 (last Sunday of Feb 2013)
    # March: 2013-03-31 (last Sunday of Mar 2013)
    # April: 2013-04-28 (last Sunday of Apr 2013)
    # May: 2013-05-26 (last Sunday of May 2013)
    # June: 2013-06-30 (last Sunday of Jun 2013)
    # July: 2013-07-28 (last Sunday of Jul 2013)
    # August: 2013-08-25 (last Sunday of Aug 2013)
    # September: 2013-09-29 (last Sunday of Sep 2013)
    # October: 2013-10-27 (last Sunday of Oct 2013)
    # November: 2013-11-24 (last Sunday of Nov 2013)
    # December: 2013-12-29 (last Sunday of Dec 2013)
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", 
        "2013-04-28", "2013-05-26", "2013-06-30", 
        "2013-07-28", "2013-08-25", "2013-09-29", 
        "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert get_last_sundays(2013) == expected

def test_get_last_sundays_for_leap_year_2032():
    # Expected values computed from the specification:
    # January: 2032-01-25 (last Sunday of Jan 2032)
    # February: 2032-02-29 (Feb 29 is a Sunday in leap year 2032)
    # March: 2032-03-28 (last Sunday of Mar 2032)
    # April: 2032-04-25 (last Sunday of Apr 2032)
    # May: 2032-05-30 (last Sunday of May 2032)
    # June: 2032-06-27 (last Sunday of Jun 2032)
    # July: 2032-07-25 (last Sunday of Jul 2032)
    # August: 2032-08-29 (last Sunday of Aug 2032)
    # September: 2032-09-26 (last Sunday of Sep 2032)
    # October: 2032-10-31 (last Sunday of Oct 2032)
    # November: 2032-11-28 (last Sunday of Nov 2032)
    # December: 2032-12-26 (last Sunday of Dec 2032)
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", 
        "2032-04-25", "2032-05-30", "2032-06-27", 
        "2032-07-25", "2032-08-29", "2032-09-26", 
        "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert get_last_sundays(2032) == expected

def test_get_last_sundays_for_century_year_2100():
    # Expected values computed from the specification:
    # January: 2100-01-31 (last Sunday of Jan 2100)
    # February: 2100-02-28 (not a leap year, last day is Feb 28)
    # March: 2100-03-28 (last Sunday of Mar 2100)
    # April: 2100-04-25 (last Sunday of Apr 2100)
    # May: 2100-05-30 (last Sunday of May 2100)
    # June: 2100-06-27 (last Sunday of Jun 2100)
    # July: 2100-07-25 (last Sunday of Jul 2100)
    # August: 2100-08-29 (last Sunday of Aug 2100)
    # September: 2100-09-26 (last Sunday of Sep 2100)
    # October: 2100-10-31 (last Sunday of Oct 2100)
    # November: 2100-11-28 (last Sunday of Nov 2100)
    # December: 2100-12-26 (last Sunday of Dec 2100)
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", 
        "2100-04-25", "2100-05-30", "2100-06-27", 
        "2100-07-25", "2100-08-29", "2100-09-26", 
        "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert get_last_sundays(2100) == expected

def test_get_last_sunday_of_month_for_january_2013():
    # Expected value computed from the specification: January 2013 gives January 27
    expected = "2013-01-27"
    assert get_last_sunday_of_month(2013, 1) == expected

def test_get_last_sunday_of_month_for_march_2013():
    # Expected value computed from the specification: March 2013 gives March 31
    expected = "2013-03-31"
    assert get_last_sunday_of_month(2013, 3) == expected

def test_get_last_sunday_of_month_for_february_2024():
    # Expected value computed from the specification: February 2024 gives February 25
    expected = "2024-02-25"
    assert get_last_sunday_of_month(2024, 2) == expected

def test_get_last_sunday_of_month_for_invalid_month():
    # Expected value: error message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        get_last_sunday_of_month(2023, 13)

def test_get_last_sunday_of_month_for_lower_bound_invalid_month():
    # Expected value: error message "month must be in 1..12"
    with pytest.raises(Exception, match=r"^month must be in 1\.\.12$"):
        get_last_sunday_of_month(2023, 0)

def test_get_last_sunday_of_month_for_december_2000():
    # Expected value computed from the specification: December 2000 gives December 31
    expected = "2000-12-31"
    assert get_last_sunday_of_month(2000, 12) == expected

def test_get_last_sundays_for_year_2000():
    # Expected values computed from the specification:
    # January: 2000-01-30 (last Sunday of Jan 2000)
    # February: 2000-02-29 (leap year, last day is Feb 29)
    # March: 2000-03-26 (last Sunday of Mar 2000)
    # April: 2000-04-30 (last Sunday of Apr 2000)
    # May: 2000-05-28 (last Sunday of May 2000)
    # June: 2000-06-25 (last Sunday of Jun 2000)
    # July: 2000-07-30 (last Sunday of Jul 2000)
    # August: 2000-08-27 (last Sunday of Aug 2000)
    # September: 2000-09-24 (last Sunday of Sep 2000)
    # October: 2000-10-29 (last Sunday of Oct 2000)
    # November: 2000-11-26 (last Sunday of Nov 2000)
    # December: 2000-12-31 (last Sunday of Dec 2000)
    expected = [
        "2000-01-30", "2000-02-29", "2000-03-26", 
        "2000-04-30", "2000-05-28", "2000-06-25", 
        "2000-07-30", "2000-08-27", "2000-09-24", 
        "2000-10-29", "2000-11-26", "2000-12-31"
    ]
    assert get_last_sundays(2000) == expected

def test_invariant_last_days_of_month():
    # Check that all last Sundays are within the last seven days of their respective months
    for year in range(2010, 2025):
        last_sundays = get_last_sundays(year)
        for month, last_sunday in enumerate(last_sundays, start=1):
            last_sunday_date = last_sunday.split('-')
            last_sunday_day = int(last_sunday_date[2])
            last_month_length = calendar.monthrange(year, month)[1]
            assert last_sunday_day >= last_month_length - 6  # Last Sunday must be in the last 7 days