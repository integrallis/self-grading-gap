# test_solution.py

from solution import last_sundays

def test_list_years_last_sundays():
    # For the year 2013:
    # January: 2013-01-27, February: 2013-02-24, March: 2013-03-31,
    # April: 2013-04-28, May: 2013-05-26, June: 2013-06-30,
    # July: 2013-07-28, August: 2013-08-25, September: 2013-09-29,
    # October: 2013-10-27, November: 2013-11-24, December: 2013-12-29
    assert last_sundays(2013) == [
        "2013-01-27", "2013-02-24", "2013-03-31", "2013-04-28", 
        "2013-05-26", "2013-06-30", "2013-07-28", "2013-08-25", 
        "2013-09-29", "2013-10-27", "2013-11-24", "2013-12-29"
    ]

def test_leap_year_with_february_29_on_sunday():
    # For the year 2032:
    # January: 2032-01-25, February: 2032-02-29, March: 2032-03-28,
    # April: 2032-04-25, May: 2032-05-30, June: 2032-06-27,
    # July: 2032-07-25, August: 2032-08-29, September: 2032-09-26,
    # October: 2032-10-31, November: 2032-11-28, December: 2032-12-26
    assert last_sundays(2032) == [
        "2032-01-25", "2032-02-29", "2032-03-28", "2032-04-25", 
        "2032-05-30", "2032-06-27", "2032-07-25", "2032-08-29", 
        "2032-09-26", "2032-10-31", "2032-11-28", "2032-12-26"
    ]

def test_leap_year_with_february_29_on_weekday():
    # For the year 2024:
    # January: 2024-01-28, February: 2024-02-25, March: 2024-03-31,
    # April: 2024-04-28, May: 2024-05-26, June: 2024-06-30,
    # July: 2024-07-28, August: 2024-08-25, September: 2024-09-29,
    # October: 2024-10-27, November: 2024-11-24, December: 2024-12-29
    assert last_sundays(2024) == [
        "2024-01-28", "2024-02-25", "2024-03-31", "2024-04-28", 
        "2024-05-26", "2024-06-30", "2024-07-28", "2024-08-25", 
        "2024-09-29", "2024-10-27", "2024-11-24", "2024-12-29"
    ]

def test_century_year_not_leap():
    # For the year 2100:
    # January: 2100-01-28, February: 2100-02-28, March: 2100-03-31,
    # April: 2100-04-30, May: 2100-05-28, June: 2100-06-30,
    # July: 2100-07-29, August: 2100-08-31, September: 2100-09-30,
    # October: 2100-10-28, November: 2100-11-30, December: 2100-12-31
    assert last_sundays(2100) == [
        "2100-01-28", "2100-02-28", "2100-03-31", "2100-04-30", 
        "2100-05-28", "2100-06-30", "2100-07-29", "2100-08-31", 
        "2100-09-30", "2100-10-28", "2100-11-30", "2100-12-31"
    ]

def test_single_month_last_sunday():
    # For January 2013, last Sunday is 2013-01-27
    assert last_sundays(2013, 1) == "2013-01-27"
    # For March 2013, last Sunday is 2013-03-31
    assert last_sundays(2013, 3) == "2013-03-31"

def test_single_month_out_of_range():
    # Month 0 is invalid
    with pytest.raises(ValueError, match="month must be in 1..12"):
        last_sundays(2023, 0)
    # Month 13 is invalid
    with pytest.raises(ValueError, match="month must be in 1..12"):
        last_sundays(2023, 13)

def test_single_month_last_sunday_within_final_days():
    # For February 2024, last Sunday is 2024-02-25
    assert last_sundays(2024, 2) == "2024-02-25"
    # For December 2024, last Sunday is 2024-12-29
    assert last_sundays(2024, 12) == "2024-12-29"