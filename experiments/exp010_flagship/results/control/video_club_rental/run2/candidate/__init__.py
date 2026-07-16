from enum import Enum

class PricingCategory(Enum):
    REGULAR = 'regular'
    NEW_RELEASE = 'new_release'
    CHILDRENS = 'childrens'

class Movie:
    def __init__(self, title, category):
        self.title = title
        self.category = category


def price_rental(category, days_rented):
    if days_rented < 1:
        raise ValueError("days_rented must be at least 1")
    if category == PricingCategory.REGULAR:
        return 2.0 + max(0, days_rented - 2) * 1.5
    elif category == PricingCategory.NEW_RELEASE:
        return 3.0 * days_rented
    elif category == PricingCategory.CHILDRENS:
        return 1.5 + max(0, days_rented - 3) * 1.5
    else:
        raise ValueError("Invalid Pricing Category")


def award_frequent_renter_points(category, days_rented):
    if category == PricingCategory.NEW_RELEASE and days_rented > 1:
        return 2
    return 1

class RentalAccount:
    def __init__(self, customer_name):
        self.customer_name = customer_name
        self.rentals = []

    def add_rental(self, movie_title, category, days_rented):
        self.rentals.append((movie_title, category, days_rented))

    def total_charge(self):
        return sum(price_rental(category, days) for _, category, days in self.rentals)

    def total_points(self):
        return sum(award_frequent_renter_points(category, days) for _, category, days in self.rentals)


def print_statement(account):
    statement = f"Rental Record for {account.customer_name}\n"
    for movie_title, category, days in account.rentals:
        statement += f"\t{movie_title}\t{price_rental(category, days)}\n"
    statement += f"Amount owed is {account.total_charge()}\n"
    statement += f"You earned {account.total_points()} frequent renter points"
    return statement
