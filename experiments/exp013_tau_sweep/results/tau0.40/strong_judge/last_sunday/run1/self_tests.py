import pytest
from solution import last_sundays

def test_last_sundays_of_year_2013():
    # Expected last Sundays for the year 2013:
    # January 27, February 24, March 31, April 28, May 26, June 30, 
    # July 28, August 25, September 29, October 27, November 24, December 29
    expected = [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28",
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25",
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]
    assert last_sundays(2013) == expected

def test_last_sundays_of_year_2032():
    # Expected last Sundays for the year 2032:
    # January 25, February 29 (leap year), March 28, April 25, 
    # May 30, June 27, July 25, August 29, September 26, 
    # October 31, November 28, December 26
    expected = [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25",
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29",
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]
    assert last_sundays(2032) == expected

def test_last_sundays_of_year_2100():
    # Expected last Sundays for the year 2100:
    # January 31, February 28, March 28, April 25, 
    # May 30, June 27, July 25, August 29, September 26, 
    # October 31, November 28, December 26
    expected = [
        "2100-01-31", "2100-02-28", "2100-03-28", "2100-04-25",
        "2100-05-30", "2100-06-27", "2100-07-25", "2100-08-29",
        "2100-09-26", "2100-10-31", "2100-11-28", "2100-12-26"
    ]
    assert last_sundays(2100) == expected

def test_last_sunday_of_specific_month_january_2013():
    # Expected last Sunday of January 2013 is January 27
    expected = "2013-01-27"
    assert last_sundays(2013, 1) == expected

def test_last_sunday_of_specific_month_february_2024():
    # Expected last Sunday of February 2024 is February 25
    expected = "2024-02-25"
    assert last_sundays(2024, 2) == expected

def test_last_sunday_of_specific_month_february_2032():
    # Expected last Sunday of February 2032 is February 29 (leap year)
    expected = "2032-02-29"
    assert last_sundays(2032, 2) == expected

def test_last_sunday_of_specific_month_march_2013():
    # Expected last Sunday of March 2013 is March 31
    expected = "2013-03-31"
    assert last_sundays(2013, 3) == expected

def test_last_sunday_of_specific_month_december_2000():
    # Expected last Sunday of December 2000 is December 31
    expected = "2000-12-31"
    assert last_sundays(2000, 12) == expected

def test_last_sunday_of_specific_month_out_of_range():
    # Expected ValueError for month out of range (13)
    with pytest.raises(ValueError, match=r"^month must be in 1\.\.12$"):
        last_sundays(2013, 13)

def test_last_sunday_of_specific_month_zero():
    # Expected ValueError for month out of range (0)
    with pytest.raises(ValueError, match=r"^month must be in 1\.\.12$"):
        last_sundays(2013, 0)