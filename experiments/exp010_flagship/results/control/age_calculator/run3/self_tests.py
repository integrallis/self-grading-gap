import pytest
from solution import calculate_age_and_birthday_week

# US-1: Age in whole years
def test_age_completed_years_example():
    # Born 28 October 2016, referenced 5 November 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "November 1, 2022")

def test_age_completed_years_before_first_anniversary():
    # Born 28 October 2016, referenced 27 October 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-10-27") == (5, "October 23, 2022")

def test_age_completed_years_on_anniversary():
    # Born 31 December 2016, referenced 1 January 2023
    assert calculate_age_and_birthday_week("2016-12-31", "2023-01-01") == (0, "December 25, 2022")

def test_age_completed_years_on_same_day():
    # Born 1 January 2000, referenced 1 January 2000
    assert calculate_age_and_birthday_week("2000-01-01", "2000-01-01") == (0, "December 26, 1999")

# US-2: Leap-day birthdays
def test_age_leap_day_birthday_non_leap_year():
    # Born 29 February 2000, referenced 28 February 2021
    assert calculate_age_and_birthday_week("2000-02-29", "2021-02-28") == (20, "February 28, 2021")

def test_age_leap_day_birthday_leap_year():
    # Born 29 February 2000, referenced 29 February 2024
    assert calculate_age_and_birthday_week("2000-02-29", "2024-02-29") == (24, "February 25, 2024")

# US-3: Future birth dates are rejected
def test_future_birth_date():
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-10-01", "2023-09-30")

def test_future_birth_date_next_day():
    with pytest.raises(ValueError, match="birthdate is after today"):
        calculate_age_and_birthday_week("2023-10-02", "2023-10-01")

# US-4: Birthday week start date
def test_birthday_week_start_thursday():
    # Born 7 September 2017, referenced 9 September 2017
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-09") == (0, "September 3, 2017")

def test_birthday_week_start_sunday():
    # Born 3 September 2017, referenced 3 September 2017
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")

def test_birthday_week_start_monday():
    # Born 4 September 2017, referenced 4 September 2017
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")

def test_birthday_week_start_wednesday():
    # Born 6 September 2017, referenced 6 September 2017
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")