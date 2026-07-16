# file: age_calculator.py

from candidate.impl import AgeCalculator
from datetime import date

def birthday_week_start(birth_date: str, reference_date: str) -> str:
    age_calculator = AgeCalculator(birth_date, reference_date)
    return age_calculator.get_birthday_week_start()

def calculate_age(birth_date: str, reference_date: str) -> int:
    age_calculator = AgeCalculator(birth_date, reference_date)
    return age_calculator.calculate_age()
