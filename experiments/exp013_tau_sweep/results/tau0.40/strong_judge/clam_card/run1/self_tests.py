# test_transit_fare_card.py

from solution import TransitFareCard

def test_journey_wholly_within_zone_a():
    card = TransitFareCard()
    fare = card.journey("Aldgate", "Anerley", "2023-10-01")  # Journey in Zone A
    assert fare == 2.50  # AC-1.1

def test_journey_touching_zone_b():
    card = TransitFareCard()
    fare = card.journey("Aldgate", "Balham", "2023-10-01")  # Journey from Zone A to Zone B
    assert fare == 3.00  # AC-1.2

def test_journey_wholly_within_zone_b():
    card = TransitFareCard()
    fare = card.journey("Balham", "Barbican", "2023-10-01")  # Journey in Zone B
    assert fare == 3.00  # AC-1.2

def test_journey_reports_charge():
    card = TransitFareCard()
    fare = card.journey("Aldgate", "Anerley", "2023-10-01")
    assert fare == 2.50  # AC-1.4

def test_daily_cap_zone_a():
    card = TransitFareCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    fare = card.journey("Aldgate", "Anerley", "2023-10-01")  # Should charge 2.00 (7.00 cap)
    assert fare == 2.00  # AC-2.1
    fare = card.journey("Aldgate", "Anerley", "2023-10-01")  # Should charge 0.00 (cap reached)
    assert fare == 0.00  # AC-2.1

def test_daily_cap_zone_b():
    card = TransitFareCard()
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    card.journey("Balham", "Barbican", "2023-10-01")  # 3.00
    fare = card.journey("Balham", "Barbican", "2023-10-01")  # Should charge 2.00 (8.00 cap)
    assert fare == 2.00  # AC-2.2
    fare = card.journey("Balham", "Barbican", "2023-10-01")  # Should charge 0.00 (cap reached)
    assert fare == 0.00  # AC-2.2

def test_daily_cap_zone_b_lifts_previous_cap_zone_a():
    card = TransitFareCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00, cap reached at 7.00
    fare = card.journey("Balham", "Barbican", "2023-10-01")  # 1.00 additional charge
    assert fare == 1.00  # AC-2.4

def test_weekly_cap_zone_a():
    card = TransitFareCard()
    for day in range(6):  # Six days in one ISO week
        for _ in range(3):  # Three journeys each day
            card.journey("Aldgate", "Anerley", f"2023-10-{day + 2:02d}")  # Journey in Zone A (from 2023-10-02 to 2023-10-07)
    assert card.total == 40.00  # AC-3.1

def test_weekly_cap_zone_b():
    card = TransitFareCard()
    for day in range(6):  # Six days in one ISO week
        for _ in range(3):  # Three journeys each day
            card.journey("Balham", "Barbican", f"2023-10-{day + 2:02d}")  # Journey in Zone B (from 2023-10-02 to 2023-10-07)
    assert card.total == 47.00  # AC-3.1

def test_monthly_cap_zone_a():
    card = TransitFareCard()
    for day in range(1, 32):  # Three journeys every day in October
        for _ in range(3):  # Three journeys each day
            card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")
    assert card.total == 145.00  # AC-3.3

def test_monthly_cap_zone_b():
    card = TransitFareCard()
    for day in range(1, 32):  # Three journeys every day in October
        for _ in range(3):  # Three journeys each day
            card.journey("Balham", "Barbican", f"2023-10-{day:02d}")
    assert card.total == 165.00  # AC-3.3

def test_unknown_station_rejection():
    card = TransitFareCard()
    with pytest.raises(Exception) as excinfo:
        card.journey("Aldgate", "UnknownStation", "2023-10-01")  # Unknown station
    assert "Unknown station: UnknownStation" in str(excinfo.value)  # AC-4.1
    assert card.total == 0.00  # AC-4.2

def test_unknown_origin_station_rejection():
    card = TransitFareCard()
    with pytest.raises(Exception) as excinfo:
        card.journey("UnknownStation", "Anerley", "2023-10-01")  # Unknown origin station
    assert "Unknown station: UnknownStation" in str(excinfo.value)  # AC-4.1
    assert card.total == 0.00  # AC-4.2

def test_rejected_journey_total_remains_unchanged():
    card = TransitFareCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    assert card.total == 2.50  # Initial total
    with pytest.raises(Exception) as excinfo:
        card.journey("Aldgate", "UnknownStation", "2023-10-01")  # Unknown station
    assert "Unknown station: UnknownStation" in str(excinfo.value)  # AC-4.1
    assert card.total == 2.50  # Total remains unchanged

def test_new_day_full_fare():
    card = TransitFareCard()
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.50
    card.journey("Aldgate", "Anerley", "2023-10-01")  # 2.00, cap reached at 7.00
    fare = card.journey("Aldgate", "Anerley", "2023-10-02")  # New day, full fare
    assert fare == 2.50  # AC-2.3

def test_weekly_cap_zone_b_monday_after_cap():
    card = TransitFareCard()
    for day in range(5):  # Five days in one ISO week
        for _ in range(3):  # Three journeys each day
            card.journey("Balham", "Barbican", f"2023-10-{day + 2:02d}")  # Journey in Zone B (from 2023-10-02 to 2023-10-06)
    fare = card.journey("Balham", "Barbican", "2023-10-09")  # Monday after reaching weekly cap
    assert fare == 3.00  # Full fare charged on Monday

def test_new_month_full_fare():
    card = TransitFareCard()
    for day in range(1, 32):  # Three journeys every day in October
        for _ in range(3):  # Three journeys each day
            card.journey("Aldgate", "Anerley", f"2023-10-{day:02d}")
    fare = card.journey("Aldgate", "Anerley", "2023-11-01")  # New month, full fare
    assert fare == 2.50  # AC-3.3