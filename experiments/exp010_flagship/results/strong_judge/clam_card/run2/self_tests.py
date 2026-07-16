# test_transit_fare_card.py

import pytest
from solution import TransitFareCard

def test_journey_within_zone_a():
    card = TransitFareCard()
    charge = card.journey("Aldgate", "Angel", "2023-10-01")
    assert charge == 2.50  # Journey within Zone A charges 2.50
    assert card.total == 2.50  # Total should be updated to 2.50

def test_journey_touching_zone_b():
    card = TransitFareCard()
    charge = card.journey("Aldgate", "Balham", "2023-10-01")
    assert charge == 3.00  # Journey touching Zone B charges 3.00
    assert card.total == 3.00  # Total should be updated to 3.00

def test_journey_wholly_within_zone_b():
    card = TransitFareCard()
    charge = card.journey("Balham", "Bison", "2023-10-01")
    assert charge == 3.00  # Journey within Zone B charges 3.00
    assert card.total == 3.00  # Total should be updated to 3.00

def test_journey_zone_b_to_zone_a():
    card = TransitFareCard()
    charge = card.journey("Balham", "Angel", "2023-10-01")
    assert charge == 3.00  # Journey from Zone B to Zone A charges 3.00
    assert card.total == 3.00  # Total should be updated to 3.00

def test_daily_cap_zone_a():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    charge = card.journey("Aldgate", "Angel", "2023-10-01")  # 2.00 (capped)
    assert charge == 2.00  # Capped at 7.00
    charge = card.journey("Aldgate", "Angel", "2023-10-01")  # 0.00 (fourth journey)
    assert charge == 0.00  # Fourth journey should charge 0.00
    assert card.total == 7.00  # Total should be 7.00

def test_daily_cap_zone_b():
    card = TransitFareCard()
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 2.00 (capped)
    assert charge == 2.00  # Capped at 8.00
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 0.00 (fourth journey)
    assert charge == 0.00  # Fourth journey should charge 0.00
    assert card.total == 8.00  # Total should be 8.00

def test_next_day_full_charge():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-02")  # Full charge again
    assert card.total == 5.00  # Total should be 5.00

def test_zone_b_journey_after_zone_a_cap():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.00 (capped)
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 1.00 difference to cap
    assert charge == 1.00  # Should charge the difference to cap at 8.00
    assert card.total == 8.00  # Total should be 8.00

def test_weekly_cap_zone_a():
    card = TransitFareCard()
    for day in range(6):  # Monday to Saturday in the same ISO week
        for _ in range(3):  # Three Zone A journeys each day
            card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50 each journey
    assert card.total == 40.00  # Total should be capped at 40.00

def test_weekly_cap_zone_b():
    card = TransitFareCard()
    for day in range(6):  # Monday to Saturday in the same ISO week
        for _ in range(3):  # Three Zone B journeys each day
            card.journey("Balham", "Bison", f"2023-10-{day + 2:02d}")  # 3.00 each journey
    assert card.total == 47.00  # Total should be capped at 47.00

def test_monthly_cap_zone_a():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days in October
        for _ in range(3):  # Three Zone A journeys each day
            card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50 each journey
    assert card.total == 145.00  # Total should be capped at 145.00

def test_monthly_cap_zone_b():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days in October
        for _ in range(3):  # Three Zone B journeys each day
            card.journey("Balham", "Bison", f"2023-10-{day:02d}")  # 3.00 each journey
    assert card.total == 165.00  # Total should be capped at 165.00

def test_unknown_station_rejection():
    card = TransitFareCard()
    charge = card.journey("Aldgate", "UnknownStation", "2023-10-01")  # Journey should be rejected
    assert charge is None  # Charge should be None
    assert card.total == 0.00  # Total should remain unchanged

def test_unknown_origin_station_rejection():
    card = TransitFareCard()
    charge = card.journey("UnknownStation", "Angel", "2023-10-01")  # Journey should be rejected
    assert charge is None  # Charge should be None
    assert card.total == 0.00  # Total should remain unchanged

def test_running_total_report():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    assert card.total == 5.50  # Total should report 5.50

def test_cap_increase_with_zone_b():
    card = TransitFareCard()
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Angel", "2023-10-01")  # 2.50
    charge = card.journey("Balham", "Bison", "2023-10-01")  # 3.00
    assert charge == 3.00  # Should charge the full fare to Zone B
    assert card.total == 8.00  # Total should be 8.00

def test_weekly_reset():
    card = TransitFareCard()
    for day in range(6):  # Monday to Saturday in the same ISO week
        for _ in range(3):  # Three Zone A journeys each day
            card.journey("Aldgate", "Angel", f"2023-10-{day + 2:02d}")  # 2.50 each journey
    assert card.total == 40.00  # Total should be capped at 40.00
    charge = card.journey("Aldgate", "Angel", "2023-10-09")  # Next Monday, full charge
    assert charge == 2.50  # Should charge full fare again
    assert card.total == 42.50  # Total should be 42.50

def test_calendar_month_boundary():
    card = TransitFareCard()
    for day in range(1, 31):  # October
        for _ in range(3):  # Three Zone A journeys each day
            card.journey("Aldgate", "Angel", f"2023-10-{day:02d}")  # 2.50 each journey
    assert card.total == 145.00  # Total should be capped at 145.00
    for day in range(1, 31):  # November
        for _ in range(3):  # Three Zone A journeys each day
            card.journey("Aldgate", "Angel", f"2023-11-{day:02d}")  # 2.50 each journey
    assert card.total == 290.00  # Total should be capped at 145.00 for October and 145.00 for November