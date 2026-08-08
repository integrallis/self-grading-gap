import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_whole_years():
    # AC-1.1
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "October 23, 2016")  # age is 6 years, week starts on the Sunday of the birthday week
    # AC-1.2
    assert calculate_age_and_birthday_week("2016-12-31", "2017-01-01") == (0, "December 25, 2016")  # age is 0 years, week starts on the Sunday before
    # AC-1.3
    assert calculate_age_and_birthday_week("2016-01-01", "2017-01-01") == (1, "December 25, 2016")  # age is 1 year, week starts on the Sunday before
    assert calculate_age_and_birthday_week("2016-01-01", "2017-01-02") == (1, "December 25, 2016")  # age is still 1 year, week starts on the Sunday before
    # AC-1.4
    assert calculate_age_and_birthday_week("2022-11-05", "2022-11-05") == (0, "October 30, 2022")  # age is 0 years, week starts on the Sunday before
    # New test for day before anniversary
    assert calculate_age_and_birthday_week("2016-10-28", "2022-10-27") == (5, "October 23, 2016")  # age is 5 years, week starts on the Sunday of the birthday week

def test_leap_day_birthdays():
    # AC-2.1
    assert calculate_age_and_birthday_week("2000-02-29", "2021-02-28") == (20, "February 23, 2021")  # age is 20 years, week starts on February 23
    assert calculate_age_and_birthday_week("2000-02-29", "2021-03-01") == (21, "February 23, 2021")  # age is 21 years, week starts on February 23
    # AC-2.2
    assert calculate_age_and_birthday_week("2000-02-29", "2020-02-29") == (20, "February 23, 2020")  # age is 20 years, week starts on February 23

def test_future_birth_dates():
    # AC-3.1
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age_and_birthday_week("2023-10-01", "2023-09-30")  # birthdate is in the future
    # AC-3.2
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age_and_birthday_week("2023-10-02", "2023-10-01")  # birthdate is the next day

def test_birthday_week_start_date():
    # AC-4.1
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")  # age is 0 years, week starts on August 28
    # AC-4.2
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")  # birthday week starts on September 3
    assert calculate_age_and_birthday_week("2017-09-08", "2017-09-08") == (0, "September 3, 2017")  # birthday week starts on September 3
    assert calculate_age_and_birthday_week("2017-09-09", "2017-09-09") == (0, "September 3, 2017")  # birthday week starts on September 3
    # AC-4.3
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")  # birthday week starts on August 29
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")  # birthday week starts on August 31