# test_birthday_service.py

from solution import calculate_age, birthday_week_start

def test_age_in_completed_years():
    # AC-1.1
    assert calculate_age("2016-10-28", "2022-11-05") == 6  # 2022 - 2016 = 6 years completed
    # AC-1.2
    assert calculate_age("2016-12-31", "2017-01-01") == 0  # Not yet reached 1 year
    # AC-1.3
    assert calculate_age("2016-10-28", "2017-10-28") == 1  # Reached 1 year on anniversary
    assert calculate_age("2016-10-28", "2017-10-29") == 1  # Day after anniversary, still 1 year
    # AC-1.4
    assert calculate_age("2016-10-28", "2016-10-28") == 0  # Birthdate equals reference date, age is 0
    assert calculate_age("2017-10-27", "2017-10-28") == 0  # Day before anniversary, still 0 years

def test_leap_day_birthdays():
    # AC-2.1
    assert calculate_age("2000-02-29", "2021-02-28") == 20  # Previous age applies, 20 years completed
    assert calculate_age("2000-02-29", "2021-03-01") == 21  # Birthday reached on March 1st in a non-leap year
    # AC-2.2
    assert calculate_age("2000-02-29", "2020-02-29") == 20  # Birthday reached on 29th February in a leap year

def test_future_birth_dates():
    # AC-3.1
    with pytest.raises(BaseException) as excinfo:
        calculate_age("2023-10-01", "2023-09-30")
    assert str(excinfo.value) == "birthdate is after today"  # Birthdate after reference date
    # AC-3.2
    assert calculate_age("2023-10-01", "2023-10-01") == 0  # Birthdate equals reference date, age is 0

def test_birthday_week_start_date():
    # AC-4.1
    assert birthday_week_start("2017-09-07") == "September 3, 2017"  # Thursday birthday, week starts Sunday
    assert birthday_week_start("2017-09-08") == "September 3, 2017"  # Friday birthday, week starts Sunday
    assert birthday_week_start("2017-09-09") == "September 3, 2017"  # Saturday birthday, week starts Sunday
    assert birthday_week_start("2017-09-03") == "August 28, 2017"  # Sunday birthday, week starts 6 days earlier
    assert birthday_week_start("2017-09-04") == "August 29, 2017"  # Monday birthday, week starts 6 days earlier
    assert birthday_week_start("2017-09-06") == "August 31, 2017"  # Wednesday birthday, week starts 6 days earlier