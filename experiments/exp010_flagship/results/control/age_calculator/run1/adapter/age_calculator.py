# file: age_calculator.py
from datetime import date

from candidate import calculate_age_and_birthday_week as _calculate_age_and_birthday_week


def calculate_age(birthdate, reference_date):
    age, _birthday_week = _calculate_age_and_birthday_week(
        str(birthdate),
        str(reference_date),
    )
    return age


def birthday_week_start(birthdate):
    _age, birthday_week = _calculate_age_and_birthday_week(
        str(birthdate),
        str(date.today()),
    )
    return birthday_week
