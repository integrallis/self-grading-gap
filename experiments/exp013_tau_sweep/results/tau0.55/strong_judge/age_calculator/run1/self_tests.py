import pytest
from solution import calculate_age_and_birthday_week

def test_age_in_completed_years():
    # AC-1.1: Born 28 October 2016, referenced 5 November 2022
    assert calculate_age_and_birthday_week("2016-10-28", "2022-11-05") == (6, "October 23, 2022")  # age is 6

    # AC-1.2: Born 31 December 2020, referenced 1 January 2021
    assert calculate_age_and_birthday_week("2020-12-31", "2021-01-01") == (0, "December 27, 2021")  # age is 0

    # AC-1.2: Born 2000-06-15, referenced 2022-06-14 (day before later anniversary)
    assert calculate_age_and_birthday_week("2000-06-15", "2022-06-14") == (21, "June 13, 2022")  # age is 21

    # AC-1.3: Born 1 January 2020, referenced 2 January 2021
    assert calculate_age_and_birthday_week("2020-01-01", "2021-01-02") == (1, "December 27, 2021")  # age is 1

    # AC-1.4: Born 15 March 1990, referenced 15 March 2022
    assert calculate_age_and_birthday_week("1990-03-15", "2022-03-15") == (32, "March 13, 2022")  # age is 32

    # AC-1.4: Born 1 January 2020, referenced 1 January 2020
    assert calculate_age_and_birthday_week("2020-01-01", "2020-01-01") == (0, "December 26, 2019")  # age is 0

def test_leap_day_birthdays():
    # AC-2.1: Born 29 February 2000, referenced 1 March 2021
    assert calculate_age_and_birthday_week("2000-02-29", "2021-03-01") == (21, "February 27, 2021")  # age is 21

    # AC-2.2: Born 29 February 2000, referenced 29 February 2004
    assert calculate_age_and_birthday_week("2000-02-29", "2004-02-29") == (4, "February 23, 2004")  # age is 4

    # AC-2.1: Born 29 February 2000, referenced 28 February 2021
    assert calculate_age_and_birthday_week("2000-02-29", "2021-02-28") == (20, "February 27, 2021")  # age is 20

def test_future_birth_dates_rejected():
    # AC-3.1: Birth date after reference date
    error = None
    try:
        calculate_age_and_birthday_week("2023-10-02", "2023-10-01")
    except Exception as e:
        error = e
    assert str(error) == "birthdate is after today"

    # AC-3.2: Birth date one day after reference date
    error = None
    try:
        calculate_age_and_birthday_week("2023-10-02", "2023-10-02")
    except Exception as e:
        error = e
    assert str(error) == "birthdate is after today"

def test_birthday_week_start_date():
    # AC-4.2: Birthday on 7 September 2017 (Thursday)
    assert calculate_age_and_birthday_week("2017-09-07", "2017-09-07") == (0, "September 3, 2017")  # week starts on Sunday

    # AC-4.3: Birthday on 3 September 2017 (Sunday)
    assert calculate_age_and_birthday_week("2017-09-03", "2017-09-03") == (0, "August 28, 2017")  # week starts six days before

    # AC-4.3: Birthday on 4 September 2017 (Monday)
    assert calculate_age_and_birthday_week("2017-09-04", "2017-09-04") == (0, "August 29, 2017")  # week starts six days before
    
    # AC-4.3: Birthday on 6 September 2017 (Wednesday)
    assert calculate_age_and_birthday_week("2017-09-06", "2017-09-06") == (0, "August 31, 2017")  # week starts six days before

    # AC-4.2: Birthday on 8 September 2017 (Friday)
    assert calculate_age_and_birthday_week("2017-09-08", "2017-09-08") == (0, "September 3, 2017")  # week starts on Sunday

    # AC-4.2: Birthday on 9 September 2017 (Saturday)
    assert calculate_age_and_birthday_week("2017-09-09", "2017-09-09") == (0, "September 3, 2017")  # week starts on Sunday