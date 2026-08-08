# test_video_rental.py

from solution import Movie, PriceRental, FrequentRenterPoints, RentalAccount, PrintRentalStatement

def test_regular_movie_rental_for_one_day():
    movie = Movie(title="Regular Movie", category="REGULAR")
    rental = PriceRental(movie=movie, days_rented=1)
    assert rental == 2.0  # Cost for 1 day is 2.0

def test_regular_movie_rental_for_two_days():
    movie = Movie(title="Regular Movie", category="REGULAR")
    rental = PriceRental(movie=movie, days_rented=2)
    assert rental == 2.0  # Cost for 2 days is 2.0

def test_regular_movie_rental_for_three_days():
    movie = Movie(title="Regular Movie", category="REGULAR")
    rental = PriceRental(movie=movie, days_rented=3)
    assert rental == 3.5  # Cost for 3 days is 2.0 + 1.5 for the extra day

def test_regular_movie_rental_for_five_days():
    movie = Movie(title="Regular Movie", category="REGULAR")
    rental = PriceRental(movie=movie, days_rented=5)
    assert rental == 6.5  # Cost for 5 days is 2.0 + (3 * 1.5) for the extra days

def test_new_release_rental_for_one_day():
    movie = Movie(title="New Release Movie", category="NEW_RELEASE")
    rental = PriceRental(movie=movie, days_rented=1)
    assert rental == 3.0  # Cost for 1 day is 3.0

def test_new_release_rental_for_three_days():
    movie = Movie(title="New Release Movie", category="NEW_RELEASE")
    rental = PriceRental(movie=movie, days_rented=3)
    assert rental == 9.0  # Cost for 3 days is 3.0 * 3

def test_childrens_movie_rental_for_one_day():
    movie = Movie(title="Children's Movie", category="CHILDRENS")
    rental = PriceRental(movie=movie, days_rented=1)
    assert rental == 1.5  # Cost for 1 day is 1.5

def test_childrens_movie_rental_for_three_days():
    movie = Movie(title="Children's Movie", category="CHILDRENS")
    rental = PriceRental(movie=movie, days_rented=3)
    assert rental == 1.5  # Cost for 3 days is 1.5

def test_childrens_movie_rental_for_four_days():
    movie = Movie(title="Children's Movie", category="CHILDRENS")
    rental = PriceRental(movie=movie, days_rented=4)
    assert rental == 3.0  # Cost for 4 days is 1.5 + 1.5 for the extra day

def test_childrens_movie_rental_for_six_days():
    movie = Movie(title="Children's Movie", category="CHILDRENS")
    rental = PriceRental(movie=movie, days_rented=6)
    assert rental == 6.0  # Cost for 6 days is 1.5 + (3 * 1.5) for the extra days

def test_rental_with_zero_days_raises_error():
    movie = Movie(title="Regular Movie", category="REGULAR")
    import pytest
    with pytest.raises(Exception) as exc:
        PriceRental(movie=movie, days_rented=0)
    assert str(exc.value) == "days_rented must be at least 1"

def test_rental_with_negative_days_raises_error():
    movie = Movie(title="Regular Movie", category="REGULAR")
    import pytest
    with pytest.raises(Exception) as exc:
        PriceRental(movie=movie, days_rented=-1)
    assert str(exc.value) == "days_rented must be at least 1"

def test_frequent_renter_points_for_one_day_regular():
    movie = Movie(title="Regular Movie", category="REGULAR")
    points = FrequentRenterPoints(movie=movie, days_rented=1)
    assert points == 1  # 1 point for any rental

def test_frequent_renter_points_for_new_release_more_than_one_day():
    movie = Movie(title="New Release Movie", category="NEW_RELEASE")
    points = FrequentRenterPoints(movie=movie, days_rented=2)
    assert points == 2  # 1 point + 1 bonus point for renting a new release more than one day

def test_frequent_renter_points_for_three_days_new_release():
    movie = Movie(title="New Release Movie", category="NEW_RELEASE")
    points = FrequentRenterPoints(movie=movie, days_rented=3)
    assert points == 2  # 1 point + 1 bonus point for renting a new release more than one day

def test_customer_account_for_multiple_rentals():
    account = RentalAccount(customer_name="John Doe")
    movie1 = Movie(title="Regular Movie", category="REGULAR")
    movie2 = Movie(title="New Release Movie", category="NEW_RELEASE")
    movie3 = Movie(title="Children's Movie", category="CHILDRENS")
    
    account.add_rental(movie1, 3)  # 3.5
    account.add_rental(movie2, 2)  # 6.0
    account.add_rental(movie3, 4)  # 3.0
    
    assert account.total_charge() == 12.5  # 3.5 + 6.0 + 3.0
    assert account.total_points() == 4  # 1 point each + 1 bonus for new release

def test_print_statement_with_no_rentals():
    account = RentalAccount(customer_name="Jane Doe")
    statement = PrintRentalStatement(account)
    expected_statement = (
        "Rental Record for Jane Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert statement == expected_statement

def test_print_statement_with_rentals():
    account = RentalAccount(customer_name="John Doe")
    movie1 = Movie(title="Regular Movie", category="REGULAR")
    movie2 = Movie(title="New Release Movie", category="NEW_RELEASE")
    
    account.add_rental(movie1, 3)  # 3.5
    account.add_rental(movie2, 2)  # 6.0
    
    statement = PrintRentalStatement(account)
    expected_statement = (
        "Rental Record for John Doe\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release Movie\t6.0\n"
        "Amount owed is 9.5\n"
        "You earned 3 frequent renter points"
    )
    assert statement == expected_statement

def test_movie_exposes_title_and_category():
    movie = Movie(title="Some Movie", category="REGULAR")
    assert movie.title == "Some Movie"
    assert movie.category == "REGULAR"

def test_movie_catalogue_contains_exactly_three_categories():
    assert set(Movie.CATEGORIES) == {"REGULAR", "NEW_RELEASE", "CHILDRENS"}