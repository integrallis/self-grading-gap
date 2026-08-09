# test_transit_fare_card.py

import pytest
from solution import TransitFareCard

def test_zone_a_journey_within_zone_a():
    card = TransitFareCard()
    fare = card.charge("Aldgate", "Anerley", "2023-10-01")
    assert fare == 2.50  # AC-1.1: Journey within Zone A charged 2.50

def test_zone_b_journey():
    card = TransitFareCard()
    fare = card.charge("Balham", "Barbican", "2023-10-01")
    assert fare == 3.00  # AC-1.2: Journey touching Zone B charged 3.00

def test_zone_a_total_charge_with_daily_cap():
    card = TransitFareCard()
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    fare = card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    assert fare == 2.00  # AC-2.1: Remaining to cap is 2.00

def test_zone_b_total_charge_with_daily_cap():
    card = TransitFareCard()
    card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    fare = card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    assert fare == 2.00  # AC-2.2: Remaining to cap is 2.00

def test_daily_cap_reset_next_day():
    card = TransitFareCard()
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.00
    fare = card.charge("Aldgate", "Anerley", "2023-10-02")  # New day, should charge full fare
    assert fare == 2.50  # AC-2.3: First journey of next day charged full fare

def test_zone_b_journey_on_capped_day_increases_cap():
    card = TransitFareCard()
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.00 (capped at 7.00)
    fare = card.charge("Balham", "Barbican", "2023-10-01")  # Zone B journey
    assert fare == 1.00  # AC-2.4: Charged the difference to lift cap to Zone B limit

def test_weekly_cap():
    card = TransitFareCard()
    for _ in range(6):  # 3 Zone A journeys a day for 6 days
        card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
        card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
        card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.00 (capped at 7.00)
    fare = card.charge("Aldgate", "Anerley", "2023-10-02")  # Should charge full fare as a new week starts
    assert fare == 2.50  # AC-3.2: First journey of new week charged full fare

def test_monthly_cap():
    card = TransitFareCard()
    for day in range(1, 31):  # 3 Zone A journeys a day for 30 days
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.50
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.50
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.00 (capped at 7.00)
    assert card.total() == 145.00  # AC-3.3: Capped at 145.00 for the month

def test_unknown_station_origin():
    card = TransitFareCard()
    with pytest.raises(Exception) as excinfo:  # Unknown error type
        card.charge("UnknownStation", "Anerley", "2023-10-01")  # AC-4.1: Journey from unknown station
    assert "UnknownStation" in str(excinfo.value)  # Error message should mention unknown station

def test_rejected_journey_does_not_charge():
    card = TransitFareCard()
    initial_total = card.total()
    try:
        card.charge("Aldgate", "UnknownStation", "2023-10-01")  # Should raise an error
    except Exception:  # Catch any unknown error
        pass  # Expected behavior
    assert card.total() == initial_total  # AC-4.2: Total remains unchanged

def test_running_total():
    card = TransitFareCard()
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    assert card.total() == 5.50  # AC-5.1: Total should reflect the sum of charges

def test_fourth_same_day_zone_a_journey():
    card = TransitFareCard()
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.charge("Aldgate", "Anerley", "2023-10-01")  # 2.00
    fare = card.charge("Aldgate", "Anerley", "2023-10-01")  # Fourth journey
    assert fare == 0.00  # After reaching cap, next charge should be 0.00

def test_fourth_same_day_zone_b_journey():
    card = TransitFareCard()
    card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
    card.charge("Balham", "Barbican", "2023-10-01")  # 2.00
    fare = card.charge("Balham", "Barbican", "2023-10-01")  # Fourth journey
    assert fare == 0.00  # After reaching cap, next charge should be 0.00

def test_parametrized_station_recognition():
    stations = [
        "Aldgate", "Amersham", "Anerley", "Angel", "Asterisk",
        "Balham", "Barbican", "Bison", "Bugel", "Bullhead"
    ]
    for station in stations:
        card = TransitFareCard()
        fare = card.charge(station, station, "2023-10-01")  # Charging for same station
        assert fare == (2.50 if station in ["Aldgate", "Amersham", "Anerley", "Angel", "Asterisk"] else 3.00)  # Check fare based on zone

def test_mixed_zone_a_to_b_journey():
    card = TransitFareCard()
    fare = card.charge("Aldgate", "Balham", "2023-10-01")  # Mixed journey
    assert fare == 3.00  # AC-1.2: Journey touching Zone B charged 3.00

def test_mixed_zone_b_to_a_journey():
    card = TransitFareCard()
    fare = card.charge("Balham", "Aldgate", "2023-10-01")  # Mixed journey
    assert fare == 3.00  # AC-1.2: Journey touching Zone B charged 3.00

def test_zone_b_weekly_cap():
    card = TransitFareCard()
    for _ in range(6):  # 3 Zone B journeys a day for 6 days
        card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
        card.charge("Balham", "Barbican", "2023-10-01")  # 3.00
        card.charge("Balham", "Barbican", "2023-10-01")  # 2.00 (capped at 8.00)
    fare = card.charge("Balham", "Barbican", "2023-10-08")  # Should charge 0.00 as week already capped at 47.00
    assert fare == 0.00  # AC-3.2: Journey in capped week should charge 0.00

def test_zone_b_monthly_cap():
    card = TransitFareCard()
    for day in range(1, 31):  # 3 Zone B journeys a day for 30 days
        card.charge("Balham", "Barbican", f"2023-10-{day:02d}")  # 3.00
        card.charge("Balham", "Barbican", f"2023-10-{day:02d}")  # 3.00
        card.charge("Balham", "Barbican", f"2023-10-{day:02d}")  # 2.00 (capped at 8.00)
    assert card.total() == 165.00  # AC-3.3: Capped at 165.00 for the month

def test_calendar_month_reset():
    card = TransitFareCard()
    for day in range(1, 31):  # 3 Zone A journeys a day for 30 days
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.50
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.50
        card.charge("Aldgate", "Anerley", f"2023-10-{day:02d}")  # 2.00 (capped at 7.00)
    fare = card.charge("Aldgate", "Anerley", "2023-11-01")  # New month, should charge full fare
    assert fare == 2.50  # AC-3.3: First journey of new month charged full fare