# file: age_calculator.py

from candidate.impl import BirthdayService
from datetime import date

def birthday_week_start(birthdate: str) -> str:
    """Exposes the birthday week start calculation."""
    reference_date = date.today().strftime('%Y-%m-%d')
    service = BirthdayService(birthdate, reference_date)
    return service.birthday_week_start()

def calculate_age(birthdate: str, reference_date: str) -> int:
    """Calculates the age in years."""
    service = BirthdayService(birthdate, reference_date)
    return service.age_in_years()
