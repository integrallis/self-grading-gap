# candidate/impl.py

from datetime import datetime, timedelta

class AgeCalculator:
    def __init__(self, birth_date: str, reference_date: str):
        self.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
        self.reference_date = datetime.strptime(reference_date, '%Y-%m-%d').date()
        self._validate_dates()

    def _validate_dates(self):
        if self.birth_date > self.reference_date:
            raise ValueError("birthdate is after today")

    def calculate_age(self) -> int:
        age = self.reference_date.year - self.birth_date.year
        has_birthday_passed = self._has_birthday_passed()
        return age - (0 if has_birthday_passed else 1)

    def _has_birthday_passed(self) -> bool:
        if self.birth_date.month < self.reference_date.month:
            return True
        elif self.birth_date.month > self.reference_date.month:
            return False
        else:
            return self.reference_date.day >= self.birth_date.day

    def get_birthday_week_start(self) -> str:
        birthday_this_year = self.birth_date.replace(year=self.reference_date.year)
        if birthday_this_year.month == 2 and birthday_this_year.day == 29:
            birthday_this_year = self._get_next_valid_birthday(birthday_this_year)

        birthday_week_start = self._calculate_birthday_week_start(birthday_this_year)
        return birthday_week_start.strftime("%B %d, %Y")

    def _get_next_valid_birthday(self, birthday: datetime.date) -> datetime.date:
        if self.reference_date.year % 4 == 0:
            return birthday
        else:
            return birthday.replace(year=birthday.year + 1, month=3, day=1)

    def _calculate_birthday_week_start(self, birthday: datetime.date) -> datetime.date:
        if birthday.weekday() in [3, 4, 5]:  # Thursday, Friday, Saturday
            return birthday - timedelta(days=birthday.weekday() + 1)  # Go back to Sunday
        else:  # Sunday, Monday, Tuesday, Wednesday
            return birthday - timedelta(days=(birthday.weekday() + 6) % 7)  # Go back to the previous Monday

# Example usage
# To calculate age and birthday week:
# age_calculator = AgeCalculator('2016-10-28', '2022-11-05')
# print(age_calculator.calculate_age())  # Output: 6
# print(age_calculator.get_birthday_week_start())  # Output: "October 30, 2022"
