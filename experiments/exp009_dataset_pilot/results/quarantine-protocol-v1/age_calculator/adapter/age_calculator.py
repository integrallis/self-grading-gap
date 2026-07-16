# file: age_calculator.py

from candidate.impl import BirthdayService
from datetime import date

def birthday_week_start(birth_date_str, reference_date_str):
    service = BirthdayService(birth_date_str, reference_date_str)
    return service.birthday_week_start()

def calculate_age(birth_date_str, reference_date_str):
    service = BirthdayService(birth_date_str, reference_date_str)
    return service.calculate_age()
