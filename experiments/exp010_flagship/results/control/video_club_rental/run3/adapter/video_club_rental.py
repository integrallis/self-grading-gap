# file: video_club_rental.py
from candidate import Customer as _Customer
from candidate import Movie
from candidate import PricingCategory as PriceCode


class Rental:
    def __init__(self, movie, days_rented):
        self.movie = movie
        self.days_rented = days_rented


class Customer:
    def __init__(self, name):
        self._customer = _Customer(name)

    def add_rental(self, rental):
        return self._customer.add_rental(rental.movie, rental.days_rented)

    def statement(self):
        return self._customer.statement()
