import pytest
from solution import Movie, Rental, Customer, PricingCategory

def test_regular_movie_rental_cost_for_one_day():
    movie = Movie("Regular Movie", PricingCategory.REGULAR)
    rental = Rental(movie, 1)
    assert rental.calculate_cost() == 2.0  # AC-1.1

def test_regular_movie_rental_cost_for_two_days():
    movie = Movie("Regular Movie", PricingCategory.REGULAR)
    rental = Rental(movie, 2)
    assert rental.calculate_cost() == 2.0  # AC-1.1

def test_regular_movie_rental_cost_for_three_days():
    movie = Movie("Regular Movie", PricingCategory.REGULAR)
    rental = Rental(movie, 3)
    assert rental.calculate_cost() == 3.5  # AC-1.1

def test_regular_movie_rental_cost_for_five_days():
    movie = Movie("Regular Movie", PricingCategory.REGULAR)
    rental = Rental(movie, 5)
    assert rental.calculate_cost() == 6.5  # AC-1.1

def test_new_release_movie_rental_cost_for_one_day():
    movie = Movie("New Release Movie", PricingCategory.NEW_RELEASE)
    rental = Rental(movie, 1)
    assert rental.calculate_cost() == 3.0  # AC-1.2

def test_new_release_movie_rental_cost_for_three_days():
    movie = Movie("New Release Movie", PricingCategory.NEW_RELEASE)
    rental = Rental(movie, 3)
    assert rental.calculate_cost() == 9.0  # AC-1.2

def test_children_movie_rental_cost_for_one_day():
    movie = Movie("Children's Movie", PricingCategory.CHILDRENS)
    rental = Rental(movie, 1)
    assert rental.calculate_cost() == 1.5  # AC-1.3

def test_children_movie_rental_cost_for_three_days():
    movie = Movie("Children's Movie", PricingCategory.CHILDRENS)
    rental = Rental(movie, 3)
    assert rental.calculate_cost() == 1.5  # AC-1.3

def test_children_movie_rental_cost_for_four_days():
    movie = Movie("Children's Movie", PricingCategory.CHILDRENS)
    rental = Rental(movie, 4)
    assert rental.calculate_cost() == 3.0  # AC-1.3

def test_children_movie_rental_cost_for_six_days():
    movie = Movie("Children's Movie", PricingCategory.CHILDRENS)
    rental = Rental(movie, 6)
    assert rental.calculate_cost() == 6.0  # AC-1.3

def test_rental_days_must_be_at_least_one_zero():
    movie = Movie("Test Movie", PricingCategory.REGULAR)
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        Rental(movie, 0)  # Expect to reject this rental

def test_rental_days_must_be_at_least_one_negative():
    movie = Movie("Test Movie", PricingCategory.REGULAR)
    with pytest.raises(ValueError, match="days_rented must be at least 1"):
        Rental(movie, -1)  # Expect to reject this rental

def test_frequent_renter_points_for_regular_movie():
    movie = Movie("Regular Movie", PricingCategory.REGULAR)
    rental = Rental(movie, 2)
    assert rental.calculate_points() == 1  # AC-2.1

def test_frequent_renter_points_for_children_movie():
    movie = Movie("Children's Movie", PricingCategory.CHILDRENS)
    rental = Rental(movie, 2)
    assert rental.calculate_points() == 1  # AC-2.1

def test_frequent_renter_points_for_new_release_one_day():
    movie = Movie("New Release Movie", PricingCategory.NEW_RELEASE)
    rental = Rental(movie, 1)
    assert rental.calculate_points() == 1  # AC-2.1

def test_frequent_renter_points_for_new_release_more_than_one_day():
    movie = Movie("New Release Movie", PricingCategory.NEW_RELEASE)
    rental = Rental(movie, 2)
    assert rental.calculate_points() == 2  # AC-2.2

def test_frequent_renter_points_for_new_release_three_days():
    movie = Movie("New Release Movie", PricingCategory.NEW_RELEASE)
    rental = Rental(movie, 3)
    assert rental.calculate_points() == 2  # AC-2.2

def test_customer_rentals_total_and_points():
    customer = Customer("John Doe")
    customer.add_rental(Rental(Movie("Regular Movie", PricingCategory.REGULAR), 3))
    customer.add_rental(Rental(Movie("New Release Movie", PricingCategory.NEW_RELEASE), 2))
    customer.add_rental(Rental(Movie("Children's Movie", PricingCategory.CHILDRENS), 4))
    
    assert customer.calculate_total_cost() == 12.5  # AC-3.1
    assert customer.calculate_total_points() == 4  # AC-3.1

def test_customer_statement_with_rentals():
    customer = Customer("John Doe")
    customer.add_rental(Rental(Movie("Regular Movie", PricingCategory.REGULAR), 3))
    customer.add_rental(Rental(Movie("New Release Movie", PricingCategory.NEW_RELEASE), 2))
    customer.add_rental(Rental(Movie("Children's Movie", PricingCategory.CHILDRENS), 4))
    
    expected_statement = (
        "Rental Record for John Doe\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release Movie\t6.0\n"
        "\tChildren's Movie\t3.0\n"
        "Amount owed is 12.5\n"
        "You earned 4 frequent renter points"
    )
    assert customer.statement() == expected_statement  # AC-4.1, AC-4.2, AC-4.3

def test_customer_statement_with_no_rentals():
    customer = Customer("John Doe")
    
    expected_statement = (
        "Rental Record for John Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert customer.statement() == expected_statement  # AC-4.4

def test_movie_exposes_title_and_category():
    movie = Movie("Test Movie", PricingCategory.REGULAR)
    assert movie.title == "Test Movie"  # AC-5.1
    assert movie.category == PricingCategory.REGULAR  # AC-5.1

def test_pricing_categories():
    categories = {PricingCategory.REGULAR, PricingCategory.NEW_RELEASE, PricingCategory.CHILDRENS}
    assert len(categories) == 3  # AC-5.2
    assert PricingCategory.REGULAR in categories  # AC-5.2
    assert PricingCategory.NEW_RELEASE in categories  # AC-5.2
    assert PricingCategory.CHILDRENS in categories  # AC-5.2