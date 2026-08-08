# your complete test file
import pytest
from solution import price_rental, award_frequent_renter_points, RentalAccount, Movie

def test_price_rental_regular_movie_one_day():
    # Regular movie, 1 day: 2.0
    assert price_rental('REGULAR', 1) == 2.0

def test_price_rental_regular_movie_two_days():
    # Regular movie, 2 days: 2.0
    assert price_rental('REGULAR', 2) == 2.0

def test_price_rental_regular_movie_three_days():
    # Regular movie, 3 days: 2.0 + 1.5 (for day 3) = 3.5
    assert price_rental('REGULAR', 3) == 3.5

def test_price_rental_regular_movie_five_days():
    # Regular movie, 5 days: 2.0 + 1.5*3 (for days 3, 4, 5) = 6.5
    assert price_rental('REGULAR', 5) == 6.5

def test_price_rental_new_release_one_day():
    # New release, 1 day: 3.0
    assert price_rental('NEW_RELEASE', 1) == 3.0

def test_price_rental_new_release_three_days():
    # New release, 3 days: 3.0*3 = 9.0
    assert price_rental('NEW_RELEASE', 3) == 9.0

def test_price_rental_children_movie_one_day():
    # Children's movie, 1 day: 1.5
    assert price_rental('CHILDRENS', 1) == 1.5

def test_price_rental_children_movie_two_days():
    # Children's movie, 2 days: 1.5
    assert price_rental('CHILDRENS', 2) == 1.5

def test_price_rental_children_movie_three_days():
    # Children's movie, 3 days: 1.5
    assert price_rental('CHILDRENS', 3) == 1.5

def test_price_rental_children_movie_four_days():
    # Children's movie, 4 days: 1.5 + 1.5 (for day 4) = 3.0
    assert price_rental('CHILDRENS', 4) == 3.0

def test_price_rental_children_movie_six_days():
    # Children's movie, 6 days: 1.5 + 1.5*3 (for days 4, 5, 6) = 6.0
    assert price_rental('CHILDRENS', 6) == 6.0

def test_price_rental_invalid_days_zero():
    # Should raise an error for 0 days
    with pytest.raises(Exception) as exc_info:
        price_rental('REGULAR', 0)
    assert str(exc_info.value) == "days_rented must be at least 1"

def test_price_rental_invalid_days_negative():
    # Should raise an error for -1 day
    with pytest.raises(Exception) as exc_info:
        price_rental('REGULAR', -1)
    assert str(exc_info.value) == "days_rented must be at least 1"

def test_award_frequent_renter_points_regular():
    # Regular movie earns 1 point
    assert award_frequent_renter_points('REGULAR', 1) == 1

def test_award_frequent_renter_points_new_release_one_day():
    # New release earns 1 point
    assert award_frequent_renter_points('NEW_RELEASE', 1) == 1

def test_award_frequent_renter_points_new_release_two_days():
    # New release earns 2 points (1 point + 1 bonus point)
    assert award_frequent_renter_points('NEW_RELEASE', 2) == 2

def test_award_frequent_renter_points_new_release_three_days():
    # New release earns 2 points (1 point + 1 bonus point)
    assert award_frequent_renter_points('NEW_RELEASE', 3) == 2

def test_award_frequent_renter_points_children_movie():
    # Children's movie earns 1 point
    assert award_frequent_renter_points('CHILDRENS', 1) == 1

def test_award_frequent_renter_points_children_movie_longer():
    # Children's movie earns 1 point, longer rental
    assert award_frequent_renter_points('CHILDRENS', 4) == 1

def test_rental_account():
    account = RentalAccount('John Doe')
    account.add_rental(Movie('Movie 1', 'REGULAR'), 3)  # 3.5
    account.add_rental(Movie('Movie 2', 'NEW_RELEASE'), 2)  # 6.0
    account.add_rental(Movie('Movie 3', 'CHILDRENS'), 4)  # 3.0

    # Total charge: 3.5 + 6.0 + 3.0 = 12.5
    assert account.total_charge() == 12.5
    # Total points: 1 + 2 + 1 = 4 points
    assert account.total_points() == 4

def test_rental_account_rental_order():
    account = RentalAccount('Jane Doe')
    account.add_rental(Movie('Movie 1', 'REGULAR'), 3)  # 3.5
    account.add_rental(Movie('Movie 2', 'NEW_RELEASE'), 2)  # 6.0

    # Rental order is verified by total count
    assert len(account.rentals) == 2  # Assuming rentals is the public API representing the list of rentals
    assert account.rentals[0].title == 'Movie 1'
    assert account.rentals[1].title == 'Movie 2'

def test_print_statement_no_rentals():
    account = RentalAccount('John Doe')
    statement = account.print_statement()
    expected_statement = (
        "Rental Record for John Doe\n"
        "Amount owed is 0.0\n"
        "You earned 0 frequent renter points"
    )
    assert statement.splitlines() == expected_statement.splitlines()

def test_print_statement_with_rentals():
    account = RentalAccount('Jane Doe')
    account.add_rental(Movie('Movie 1', 'REGULAR'), 3)  # 3.5
    account.add_rental(Movie('Movie 2', 'NEW_RELEASE'), 2)  # 6.0

    statement = account.print_statement()
    expected_statement = (
        "Rental Record for Jane Doe\n"
        "\tMovie 1\t3.5\n"
        "\tMovie 2\t6.0\n"
        "Amount owed is 9.5\n"
        "You earned 3 frequent renter points"
    )
    assert statement.splitlines() == expected_statement.splitlines()

def test_movie_exposes_title_and_category():
    movie = Movie("Inception", "NEW_RELEASE")
    assert movie.title == "Inception"
    assert movie.category == "NEW_RELEASE"

def test_movie_catalogue_categories():
    categories = {'REGULAR', 'NEW_RELEASE', 'CHILDRENS'}
    assert 'REGULAR' in categories
    assert 'NEW_RELEASE' in categories
    assert 'CHILDRENS' in categories
    assert len(categories) == 3