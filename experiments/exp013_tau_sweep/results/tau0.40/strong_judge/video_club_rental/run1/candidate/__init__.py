class Movie:
    def __init__(self, title, category):
        self.title = title
        self.category = category

class Rental:
    def __init__(self, movie, days_rented):
        if days_rented < 1:
            raise Exception("days_rented must be at least 1")
        self.movie = movie
        self.days_rented = days_rented

    def price(self):
        if self.movie.category == "REGULAR":
            if self.days_rented <= 2:
                return 2.0
            elif self.days_rented == 3:
                return 3.5
            else:
                return 3.5 + (self.days_rented - 3) * 1.5
        elif self.movie.category == "NEW_RELEASE":
            return self.days_rented * 3.0
        elif self.movie.category == "CHILDRENS":
            if self.days_rented <= 3:
                return 1.5
            else:
                return 1.5 + (self.days_rented - 3) * 1.5

    def frequent_renter_points(self):
        if self.movie.category == "NEW_RELEASE" and self.days_rented > 1:
            return 2
        return 1

class Customer:
    def __init__(self, name):
        self.name = name
        self.rentals_list = []

    def add_rental(self, rental):
        self.rentals_list.append(rental)

    def total_charge(self):
        return sum((rental.price() for rental in self.rentals_list), 0.0)

    def total_points(self):
        return sum(rental.frequent_renter_points() for rental in self.rentals_list)

    def rentals(self):
        return self.rentals_list

    def statement(self):
        result = [f"Rental Record for {self.name}"]
        for rental in self.rentals_list:
            result.append(f"\t{rental.movie.title}\t{rental.price()}")
        result.append(f"Amount owed is {self.total_charge() + self.total_points()}")
        display_points = self.total_points() + (1 if self.rentals_list else 0)
        result.append(f"You earned {display_points} frequent renter points")
        return '\n'.join(result)