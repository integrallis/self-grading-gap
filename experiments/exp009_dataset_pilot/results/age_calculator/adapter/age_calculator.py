# file: age_calculator.py
from datetime import date
from candidate.impl import BirthdayService


def calculate_age(birthdate, reference_date):
    return BirthdayService(str(birthdate), str(reference_date)).calculate_age()


def birthday_week_start(birthdate):
    return BirthdayService(str(birthdate), str(date.today())).birthday_week_start()
