import pytest
from solution import calculate_age, birthday_week_start

# Test age in whole years
def test_age_completed_years_example():
    # Born on 28 October 2016, referenced on 5 November 2022
    assert calculate_age('2016-10-28', '2022-11-05') == 6

def test_age_zero_before_first_anniversary():
    # Born on 28 October 2016, referenced on 27 October 2017
    assert calculate_age('2016-10-28', '2017-10-27') == 0

def test_age_stays_same_before_anniversary():
    # Born on 28 October 2016, referenced on 1 January 2017
    assert calculate_age('2016-10-28', '2017-01-01') == 0

def test_age_increments_on_anniversary():
    # Born on 28 October 2016, referenced on 28 October 2022
    assert calculate_age('2016-10-28', '2022-10-28') == 6

def test_age_stays_same_the_day_after_anniversary():
    # Born on 28 October 2016, referenced on 29 October 2022
    assert calculate_age('2016-10-28', '2022-10-29') == 6

def test_age_zero_when_birth_date_equals_reference_date():
    # Born on 28 October 2022, referenced on 28 October 2022
    assert calculate_age('2022-10-28', '2022-10-28') == 0

def test_age_for_leap_day_birthday_in_non_leap_year():
    # Born on 29 February 2000, referenced on 28 February 2021
    assert calculate_age('2000-02-29', '2021-02-28') == 20

def test_age_for_leap_day_birthday_in_leap_year():
    # Born on 29 February 2000, referenced on 29 February 2020
    assert calculate_age('2000-02-29', '2020-02-29') == 20

def test_birth_date_before_reference_date():
    # Birth date is after the reference date
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age('2023-10-02', '2023-10-01')

def test_future_birth_date():
    # Birth date is after the reference date
    with pytest.raises(Exception, match=r"^birthdate is after today$"):
        calculate_age('2023-10-01', '2023-09-30')

# Test birthday week start date
def test_birthday_week_start_before_sunday():
    # Born on 3 September 2017, birthday week starts on 28 August 2017
    assert birthday_week_start('2017-09-03') == "August 28, 2017"

def test_birthday_week_start_on_sunday():
    # Born on 3 September 2017, birthday week starts on 28 August 2017
    assert birthday_week_start('2017-09-03') == "August 28, 2017"

def test_birthday_week_start_on_monday():
    # Born on 4 September 2017, birthday week starts on 29 August 2017
    assert birthday_week_start('2017-09-04') == "August 29, 2017"

def test_birthday_week_start_on_wednesday():
    # Born on 6 September 2017, birthday week starts on 31 August 2017
    assert birthday_week_start('2017-09-06') == "August 31, 2017"

def test_birthday_week_start_on_thursday():
    # Born on 7 September 2017, birthday week starts on 3 September 2017
    assert birthday_week_start('2017-09-07') == "September 3, 2017"

def test_birthday_week_start_on_friday():
    # Born on 8 September 2017, birthday week starts on 3 September 2017
    assert birthday_week_start('2017-09-08') == "September 3, 2017"

def test_birthday_week_start_on_saturday():
    # Born on 9 September 2017, birthday week starts on 3 September 2017
    assert birthday_week_start('2017-09-09') == "September 3, 2017"