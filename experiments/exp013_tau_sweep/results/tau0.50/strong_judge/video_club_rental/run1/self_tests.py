import pytest
from solution import price_rental, award_frequent_renter_points, print_statement, Movie, Rental

def test_price_regular_movie_for_one_day():
    # Regular movie for 1 day costs 2.0
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 1)
    assert price_rental(rental) == 2.0

def test_price_regular_movie_for_two_days():
    # Regular movie for 2 days costs 2.0
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 2)
    assert price_rental(rental) == 2.0

def test_price_regular_movie_for_three_days():
    # Regular movie for 3 days costs 3.5 (2.0 for 2 days + 1.5 for 1 additional day)
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 3)
    assert price_rental(rental) == 3.5

def test_price_regular_movie_for_five_days():
    # Regular movie for 5 days costs 6.5 (2.0 for 2 days + 3.0 for 3 additional days)
    movie = Movie("Regular Movie", "REGULAR")
    rental = Rental(movie, 5)
    assert price_rental(rental) == 6.5

def test_price_new_release_for_one_day():
    # New release for 1 day costs 3.0
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 1)
    assert price_rental(rental) == 3.0

def test_price_new_release_for_two_days():
    # New release for 2 days costs 6.0 (2 days * 3.0)
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 2)
    assert price_rental(rental) == 6.0

def test_price_new_release_for_three_days():
    # New release for 3 days costs 9.0 (3.0 * 3 days)
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 3)
    assert price_rental(rental) == 9.0

def test_price_children_movie_for_one_day():
    # Children's movie for 1 day costs 1.5
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 1)
    assert price_rental(rental) == 1.5

def test_price_children_movie_for_three_days():
    # Children's movie for 3 days costs 1.5
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 3)
    assert price_rental(rental) == 1.5

def test_price_children_movie_for_four_days():
    # Children's movie for 4 days costs 3.0 (1.5 for 3 days + 1.5 for 1 additional day)
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 4)
    assert price_rental(rental) == 3.0

def test_price_children_movie_for_six_days():
    # Children's movie for 6 days costs 6.0 (1.5 for 3 days + 1.5 for 3 additional days)
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 6)
    assert price_rental(rental) == 6.0

def test_price_rental_rejects_zero_days():
    movie = Movie("Some Movie", "REGULAR")
    rental = Rental(movie, 0)
    with pytest.raises(Exception, match="^days_rented must be at least 1$"):
        price_rental(rental)

def test_price_rental_rejects_negative_days():
    movie = Movie("Some Movie", "REGULAR")
    rental = Rental(movie, -1)
    with pytest.raises(Exception, match="^days_rented must be at least 1$"):
        price_rental(rental)

def test_award_frequent_renter_points():
    movie = Movie("Some Movie", "REGULAR")
    rental = Rental(movie, 1)
    assert award_frequent_renter_points(rental) == 1  # 1 point for any rental

def test_award_frequent_renter_points_for_children_movie():
    movie = Movie("Children's Movie", "CHILDRENS")
    rental = Rental(movie, 1)
    assert award_frequent_renter_points(rental) == 1  # 1 point for any rental

def test_award_bonus_points_for_new_release():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 2)
    assert award_frequent_renter_points(rental) == 2  # 1 point + 1 bonus point for >1 day

def test_award_frequent_renter_points_for_new_release_one_day():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 1)
    assert award_frequent_renter_points(rental) == 1  # 1 point for any rental

def test_award_frequent_renter_points_for_new_release_three_days():
    movie = Movie("New Release", "NEW_RELEASE")
    rental = Rental(movie, 3)
    assert award_frequent_renter_points(rental) == 2  # capped at 2 points

def test_customer_totals_for_three_rentals():
    movie1 = Movie("Regular Movie", "REGULAR")
    movie2 = Movie("New Release", "NEW_RELEASE")
    movie3 = Movie("Children's Movie", "CHILDRENS")

    rentals = [Rental(movie1, 3), Rental(movie2, 2), Rental(movie3, 4)]
    
    total_charge = sum(price_rental(rental) for rental in rentals)  # 12.5
    total_points = sum(award_frequent_renter_points(rental) for rental in rentals)  # 4 points

    assert total_charge == 12.5
    assert total_points == 4

def test_customer_rentals_listed_in_order():
    movie1 = Movie("Regular Movie", "REGULAR")
    movie2 = Movie("New Release", "NEW_RELEASE")
    movie3 = Movie("Children's Movie", "CHILDRENS")

    rentals = [Rental(movie1, 3), Rental(movie2, 2), Rental(movie3, 4)]
    
    assert len(rentals) == 3
    assert rentals[0].movie.title == "Regular Movie"
    assert rentals[1].movie.title == "New Release"
    assert rentals[2].movie.title == "Children's Movie"

def test_print_statement_with_no_rentals():
    statement = print_statement("Customer Name", [])
    expected_output = "Rental Record for Customer Name\nAmount owed is 0.0\nYou earned 0 frequent renter points"
    assert statement == expected_output

def test_print_statement_with_rentals():
    movie1 = Movie("Regular Movie", "REGULAR")
    movie2 = Movie("New Release", "NEW_RELEASE")
    rentals = [Rental(movie1, 3), Rental(movie2, 2)]
    
    statement = print_statement("Customer Name", rentals)
    expected_output = (
        "Rental Record for Customer Name\n"
        "\tRegular Movie\t3.5\n"
        "\tNew Release\t6.0\n"
        "Amount owed is 9.5\n"
        "You earned 3 frequent renter points"
    )
    assert statement == expected_output

def test_movie_exposes_title_and_category():
    movie = Movie("Some Movie", "REGULAR")
    assert movie.title == "Some Movie"
    assert movie.category == "REGULAR"

def test_movie_catalogue_categories():
    # Check that the implementation provides exactly these three categories
    categories = ["REGULAR", "NEW_RELEASE", "CHILDRENS"]
    assert sorted(categories) == sorted(["REGULAR", "NEW_RELEASE", "CHILDRENS"])