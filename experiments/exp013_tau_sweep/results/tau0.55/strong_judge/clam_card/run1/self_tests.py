import pytest
from solution import TransitFareCard

def test_journey_wholly_within_zone_a():
    card = TransitFareCard()
    charge = card.journey("Aldgate", "Angel", "2023-10-01")
    assert charge == 2.50  # AC-1.1

def test_journey_wholly_within_zone_b():
    card = TransitFareCard()
    charge = card.journey("Balham", "Bison", "2023-10-01")
    assert charge == 3.00  # AC-1.2

def test_journey_touching_zone_b():
    card = TransitFareCard()
    charge = card.journey("Aldgate", "Balham", "2023-10-01")
    assert charge == 3.00  # AC-1.2

def test_journey_with_unknown_station():
    card = TransitFareCard()
    with pytest.raises(Exception) as excinfo:
        card.journey("UnknownStation", "Angel", "2023-10-01")
    assert "UnknownStation" in str(excinfo.value)  # AC-4.1

def test_journey_with_unknown_destination_station():
    card = TransitFareCard()
    with pytest.raises(Exception) as excinfo:
        card.journey("Aldgate", "UnknownStation", "2023-10-01")
    assert "UnknownStation" in str(excinfo.value)  # AC-4.1

def test_daily_cap_zone_a():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    charge = card.journey("Aldgate", "Angel", "2023-10-01")  # 2.00, capped at 7.00
    assert charge == 2.00  # AC-2.1
    charge = card.journey("Aldgate", "Angel", "2023-10-01")  # 0.00, already capped
    assert charge == 0.00  # AC-2.1

def test_daily_cap_zone_b():
    card = TransitFareCard()
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 2.00, capped at 8.00
    assert charge == 2.00  # AC-2.2
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 0.00, already capped
    assert charge == 0.00  # AC-2.2

def test_daily_cap_zone_a_to_b():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50, capped at 7.00
    charge = card.journey("Aldgate", "Balham", "2023-10-01")  # 1.00 difference to 8.00 cap
    assert charge == 1.00  # AC-2.4

def test_weekly_cap_zone_a():
    card = TransitFareCard()
    for day in range(6):  # 3 journeys for 6 days
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
    assert card.total() == 40.00  # AC-3.1

def test_weekly_cap_zone_b():
    card = TransitFareCard()
    for day in range(6):  # 3 journeys for 6 days
        card.journey("Balham", "Bison", f"2023-10-{day + 2:02d}")  # 3.00
        card.journey("Balham", "Bison", f"2023-10-{day + 2:02d}")  # 3.00
        card.journey("Balham", "Bison", f"2023-10-{day + 2:02d}")  # 3.00
    assert card.total() == 47.00  # AC-3.2

def test_weekly_cap_reset_on_monday():
    card = TransitFareCard()
    for day in range(5):  # 3 journeys for 5 days
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50
    charge = card.journey("Aldgate", "Angel", "2023-10-09")  # New week, should charge full fare
    assert charge == 2.50  # AC-3.2

def test_monthly_cap_zone_a():
    card = TransitFareCard()
    for day in range(1, 31):  # 3 journeys every day for a month
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
    assert card.total() == 145.00  # AC-3.3

def test_monthly_cap_zone_b():
    card = TransitFareCard()
    for day in range(1, 31):  # 3 journeys every day for a month
        card.journey("Balham", "Bison", f"2023-10-{day:02d}")  # 3.00
        card.journey("Balham", "Bison", f"2023-10-{day:02d}")  # 3.00
        card.journey("Balham", "Bison", f"2023-10-{day:02d}")  # 3.00
    assert card.total() == 165.00  # AC-3.3

def test_monthly_cap_spanning_two_months():
    card = TransitFareCard()
    for day in range(1, 29):  # 3 journeys every day for October
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50
    for day in range(1, 2):  # 3 journeys on November 1st
        card.journey("Aldgate", "Angel", f"2023-11-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-11-{day:02d}")  # 2.50
        card.journey("Aldgate", "Angel", f"2023-11-{day:02d}")  # 2.50
    # October's cap was 145.00, November's should charge normally
    assert card.total() == 145.00 + 7.50  # AC-3.3

def test_running_total():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    assert card.total() == 5.50  # AC-5.1
    card.journey("Aldgate", "Angel", "2023-10-02")  # 2.50
    assert card.total() == 8.00  # AC-5.1