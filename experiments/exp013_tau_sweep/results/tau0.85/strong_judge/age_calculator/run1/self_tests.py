import pytest
from solution import calculate_age, birthday_week_start

# US-1: Age in whole years
def test_age_on_anniversary():
    # born 28 October 2016, referenced on 5 November 2022 -> age is 6
    assert calculate_age("2016-10-28", "2022-11-05") == 6

def test_age_before_first_anniversary():
    # born 28 October 2016, referenced on 27 October 2017 -> age is 0
    assert calculate_age("2016-10-28", "2017-10-27") == 0

def test_age_on_birthday():
    # born 31 December 2016, referenced on 1 January 2017 -> age is 0
    assert calculate_age("2016-12-31", "2017-01-01") == 0

def test_age_crossing_new_year():
    # born 31 December 2016, referenced on 1 January 2018 -> age is 1
    assert calculate_age("2016-12-31", "2018-01-01") == 1

def test_age_when_birthdate_equals_reference():
    # born 28 October 2016, referenced on 28 October 2016 -> age is 0
    assert calculate_age("2016-10-28", "2016-10-28") == 0

def test_age_on_anniversary_increment():
    # born 28 October 2016, referenced on 28 October 2017 -> age is 1
    assert calculate_age("2016-10-28", "2017-10-28") == 1

def test_age_day_after_anniversary():
    # born 28 October 2016, referenced on 29 October 2017 -> age is 1
    assert calculate_age("2016-10-28", "2017-10-29") == 1

# US-2: Leap-day birthdays
def test_age_non_leap_year():
    # born 29 February 2000, referenced on 28 February 2021 -> age is 20
    assert calculate_age("2000-02-29", "2021-02-28") == 20

def test_age_leap_year():
    # born 29 February 2000, referenced on 29 February 2020 -> age is 20
    assert calculate_age("2000-02-29", "2020-02-29") == 20

def test_age_leap_day_transition():
    # born 29 February 2000, referenced on 1 March 2021 -> age is 21
    assert calculate_age("2000-02-29", "2021-03-01") == 21

def test_age_leap_day_previous():
    # born 29 February 2000, referenced on 28 February 2020 -> age is 19
    assert calculate_age("2000-02-29", "2020-02-28") == 19

# US-3: Future birth dates are rejected
def test_future_birthdate():
    # birth date equals reference date, should not raise an error
    assert calculate_age("2023-10-01", "2023-10-01") == 0

def test_future_birthdate_one_day_after():
    # birth date after reference date, should raise an error
    with pytest.raises(Exception) as exc_info:
        calculate_age("2023-10-02", "2023-10-01")
    assert str(exc_info.value) == "birthdate is after today"

# US-4: Birthday week start date
def test_birthday_week_start_sunday():
    # birthday on 3 September 2017 (Sunday) -> week starts on 28 August 2017
    assert birthday_week_start("2017-09-03") == "August 28, 2017"

def test_birthday_week_start_monday():
    # birthday on 4 September 2017 (Monday) -> week starts on 29 August 2017
    assert birthday_week_start("2017-09-04") == "August 29, 2017"

def test_birthday_week_start_wednesday():
    # birthday on 6 September 2017 (Wednesday) -> week starts on 31 August 2017
    assert birthday_week_start("2017-09-06") == "August 31, 2017"

def test_birthday_week_start_thursday():
    # birthday on 7 September 2017 (Thursday) -> week starts on 3 September 2017
    assert birthday_week_start("2017-09-07") == "September 3, 2017"

def test_birthday_week_start_friday():
    # birthday on 8 September 2017 (Friday) -> week starts on 3 September 2017
    assert birthday_week_start("2017-09-08") == "September 3, 2017"

def test_birthday_week_start_saturday():
    # birthday on 9 September 2017 (Saturday) -> week starts on 3 September 2017
    assert birthday_week_start("2017-09-09") == "September 3, 2017"