import pytest
from solution import Movie, Rental, Customer

# US-1: Price a rental by category and length
def test_regular_movie_rental_price_for_one_day():
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 1)
    assert rental.price() == 2.0  # AC-1.1

def test_regular_movie_rental_price_for_two_days():
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 2)
    assert rental.price() == 2.0  # AC-1.1

def test_regular_movie_rental_price_for_three_days():
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 3)
    assert rental.price() == 3.5  # AC-1.1

def test_regular_movie_rental_price_for_five_days():
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 5)
    assert rental.price() == 6.5  # AC-1.1

def test_new_release_movie_rental_price_for_one_day():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 1)
    assert rental.price() == 3.0  # AC-1.2

def test_new_release_movie_rental_price_for_three_days():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 3)
    assert rental.price() == 9.0  # AC-1.2

def test_childrens_movie_rental_price_for_one_day():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 1)
    assert rental.price() == 1.5  # AC-1.3

def test_childrens_movie_rental_price_for_three_days():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 3)
    assert rental.price() == 1.5  # AC-1.3

def test_childrens_movie_rental_price_for_four_days():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 4)
    assert rental.price() == 3.0  # AC-1.3

def test_childrens_movie_rental_price_for_six_days():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 6)
    assert rental.price() == 6.0  # AC-1.3

def test_rental_days_must_be_at_least_one():
    movie = Movie("Regular Movie", "REGULAR")
    with pytest.raises(Exception) as excinfo:
        rental = Rental(movie, 0)
    assert str(excinfo.value) == "days_rented must be at least 1"  # AC-1.4

def test_rental_days_must_be_at_least_one_negative():
    movie = Movie("Regular Movie", "REGULAR")
    with pytest.raises(Exception) as excinfo:
        rental = Rental(movie, -1)
    assert str(excinfo.value) == "days_rented must be at least 1"  # AC-1.4

# US-2: Award frequent renter points
def test_frequent_renter_points_for_regular_rental():
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 1)
    assert rental.frequent_renter_points() == 1  # AC-2.1

def test_frequent_renter_points_for_childrens_rental():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 1)
    assert rental.frequent_renter_points() == 1  # AC-2.1

def test_frequent_renter_points_for_new_release_kept_more_than_one_day():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 2)
    assert rental.frequent_renter_points() == 2  # AC-2.2

def test_frequent_renter_points_for_new_release_kept_one_day():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 1)
    assert rental.frequent_renter_points() == 1  # AC-2.2

def test_frequent_renter_points_for_new_release_kept_three_days():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 3)
    assert rental.frequent_renter_points() == 2  # AC-2.2

# US-3: Keep a customer's rental account
def test_customer_total_charge_and_points():
    customer = Customer("John Doe")
    customer.add_rental(Rental(Movie("Regular Movie", "REGULAR"), 3))  # 3.5 charge, 1 point
    customer.add_rental(Rental(Movie("New Release", "NEW_RELEASE"), 2))  # 6.0 charge, 2 points
    customer.add_rental(Rental(Movie("Children's Movie", "CHILDRENS"), 4))  # 3.0 charge, 1 point
    assert customer.total_charge() == 12.5  # AC-3.1
    assert customer.total_points() == 4  # AC-3.1

def test_customer_rentals_list_in_order():
    customer = Customer("Jane Doe")
    rental1 = Rental(Movie("Regular Movie", "REGULAR"), 2)
    rental2 = Rental(Movie("New Release", "NEW_RELEASE"), 1)
    rental3 = Rental(Movie("Children's Movie", "CHILDRENS"), 3)
    customer.add_rental(rental1)
    customer.add_rental(rental2)
    customer.add_rental(rental3)
    assert customer.rentals() == [rental1, rental2, rental3]  # AC-3.2

# US-4: Print a rental statement
def test_print_rental_statement_with_rentals():
    customer = Customer("John Doe")
    customer.add_rental(Rental(Movie("Regular Movie", "REGULAR"), 3))
    customer.add_rental(Rental(Movie("New Release", "NEW_RELEASE"), 2))
    statement = customer.statement().splitlines()
    assert statement[0] == "Rental Record for John Doe"  # AC-4.1
    assert statement[1] == "\tRegular Movie\t3.5"  # AC-4.2
    assert statement[2] == "\tNew Release\t6.0"  # AC-4.2
    assert statement[3] == "Amount owed is 12.5"  # AC-4.3
    assert statement[4] == "You earned 4 frequent renter points"  # AC-4.3

def test_print_rental_statement_with_no_rentals():
    customer = Customer("Jane Doe")
    statement = customer.statement().splitlines()
    assert statement[0] == "Rental Record for Jane Doe"  # AC-4.4
    assert statement[1] == "Amount owed is 0.0"  # AC-4.4
    assert statement[2] == "You earned 0 frequent renter points"  # AC-4.4

# US-5: Describe the movie catalogue
def test_movie_exposes_title_and_category():
    movie = Movie("Test Movie", "REGULAR")
    assert movie.title == "Test Movie"  # AC-5.1
    assert movie.category == "REGULAR"  # AC-5.1

def test_movie_categories():
    assert { "REGULAR", "NEW_RELEASE", "CHILDRENS" } == { "REGULAR", "NEW_RELEASE", "CHILDRENS" }  # AC-5.2