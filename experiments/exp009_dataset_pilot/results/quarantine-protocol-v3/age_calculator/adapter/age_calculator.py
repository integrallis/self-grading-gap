# file: age_calculator.py
from candidate.impl import BirthdayService


def calculate_age(birth_date, reference_date):
    return BirthdayService(str(birth_date), str(reference_date)).calculate_age()


def birthday_week_start(birth_date):
    return BirthdayService(str(birth_date), str(birth_date)).birthday_week_start()
