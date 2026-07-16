# file: age_calculator.py
from candidate import calculate_age_and_birthday_week


def calculate_age(birthdate, reference_date):
    age, birthday_week = calculate_age_and_birthday_week(birthdate, reference_date)
    return age


def birthday_week_start(birthdate, reference_date):
    age, birthday_week = calculate_age_and_birthday_week(birthdate, reference_date)
    return birthday_week
