# file: video_club_rental.py
from candidate import Movie
from candidate import PricingCategory as PriceCode
from candidate import RentalAccount
from candidate import print_statement


class Rental:
    def __init__(self, movie, days_rented):
        self.movie = movie
        self.days_rented = days_rented


class Customer:
    def __init__(self, name):
        self.account = RentalAccount(name)

    def add_rental(self, rental):
        return self.account.add_rental(
            rental.movie.title,
            rental.movie.category,
            rental.days_rented,
        )

    def statement(self):
        return print_statement(self.account)
