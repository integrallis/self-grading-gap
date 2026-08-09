# test_transit_fare_card.py

from solution import TransitFareCard

def test_wholly_within_zone_a():
    card = TransitFareCard()
    charge = card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    assert charge == 2.50  # Journey within Zone A

def test_wholly_within_zone_b():
    card = TransitFareCard()
    charge = card.journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    assert charge == 3.00  # Journey within Zone B

def test_touching_zone_b():
    card = TransitFareCard()
    charge = card.journey('Aldgate', 'Balham', '2023-10-01')  # 3.00
    assert charge == 3.00  # Journey touching Zone B

def test_daily_cap_zone_a():
    card = TransitFareCard()
    charge1 = card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    assert charge1 == 2.50  # First journey
    charge2 = card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    assert charge2 == 2.50  # Second journey
    charge3 = card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.00
    assert charge3 == 2.00  # Third journey, daily cap of 7.00 reached
    charge4 = card.journey('Aldgate', 'Angel', '2023-10-01')  # 0.00
    assert charge4 == 0.00  # Fourth journey charges nothing

def test_daily_cap_zone_b():
    card = TransitFareCard()
    charge1 = card.journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    assert charge1 == 3.00  # First journey
    charge2 = card.journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    assert charge2 == 3.00  # Second journey
    charge3 = card.journey('Balham', 'Barbican', '2023-10-01')  # 2.00
    assert charge3 == 2.00  # Third journey, daily cap of 8.00 reached
    charge4 = card.journey('Balham', 'Barbican', '2023-10-01')  # 0.00
    assert charge4 == 0.00  # Fourth journey charges nothing

def test_daily_cap_zone_a_to_b():
    card = TransitFareCard()
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.00
    charge = card.journey('Aldgate', 'Balham', '2023-10-01')  # 1.00
    assert charge == 1.00  # Daily cap lifted to Zone B cap

def test_first_journey_next_day():
    card = TransitFareCard()
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    charge = card.journey('Aldgate', 'Angel', '2023-10-02')  # 2.50
    assert charge == 2.50  # Full fare charged on new day

def test_weekly_cap_zone_a():
    card = TransitFareCard()
    for _ in range(3):  # 3 journeys for 6 days
        card.journey('Aldgate', 'Angel', '2023-10-02')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-03')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-04')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-05')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-06')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-07')  # 2.50
    assert card.total() == 40.00  # Weekly cap reached

def test_weekly_cap_zone_b():
    card = TransitFareCard()
    for _ in range(3):  # 3 journeys for 6 days
        card.journey('Balham', 'Barbican', '2023-10-02')  # 3.00
        card.journey('Balham', 'Barbican', '2023-10-03')  # 3.00
        card.journey('Balham', 'Barbican', '2023-10-04')  # 3.00
        card.journey('Balham', 'Barbican', '2023-10-05')  # 3.00
        card.journey('Balham', 'Barbican', '2023-10-06')  # 3.00
        card.journey('Balham', 'Barbican', '2023-10-07')  # 3.00
    assert card.total() == 47.00  # Weekly cap reached

def test_monthly_cap_zone_a():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days, 3 journeys per day
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.50
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.50
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.00
    assert card.total() == 145.00  # Monthly cap reached

def test_monthly_cap_zone_b():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days, 3 journeys per day
        card.journey('Balham', 'Barbican', f'2023-10-{day:02d}')  # 3.00
        card.journey('Balham', 'Barbican', f'2023-10-{day:02d}')  # 3.00
        card.journey('Balham', 'Barbican', f'2023-10-{day:02d}')  # 2.00
    assert card.total() == 165.00  # Monthly cap reached

def test_weekly_reset_on_monday():
    card = TransitFareCard()
    for _ in range(3):  # 3 journeys for 6 days
        card.journey('Aldgate', 'Angel', '2023-10-02')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-03')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-04')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-05')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-06')  # 2.50
        card.journey('Aldgate', 'Angel', '2023-10-07')  # 2.50
    assert card.total() == 40.00  # Weekly cap reached
    charge = card.journey('Aldgate', 'Angel', '2023-10-09')  # 2.50
    assert charge == 2.50  # Full fare charged on new week

def test_calendar_month_reset():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days, 3 journeys per day in October
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.50
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.50
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.00
    assert card.total() == 145.00  # Monthly cap reached
    charge = card.journey('Aldgate', 'Angel', '2023-11-01')  # 2.50
    assert charge == 2.50  # Full fare charged in new month

def test_mixed_zone_weekly_cap():
    card = TransitFareCard()
    for _ in range(3):  # 3 journeys for 6 days, mixed zones
        card.journey('Aldgate', 'Angel', '2023-10-02')  # 2.50
        card.journey('Balham', 'Barbican', '2023-10-03')  # 3.00
        card.journey('Aldgate', 'Angel', '2023-10-04')  # 2.50
        card.journey('Balham', 'Barbican', '2023-10-05')  # 3.00
        card.journey('Aldgate', 'Angel', '2023-10-06')  # 2.50
        card.journey('Balham', 'Barbican', '2023-10-07')  # 3.00
    assert card.total() == 47.00  # Weekly cap reached

def test_mixed_zone_monthly_cap():
    card = TransitFareCard()
    for day in range(1, 31):  # 30 distinct days, mixed zones
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.50
        card.journey('Balham', 'Barbican', f'2023-10-{day:02d}')  # 3.00
        card.journey('Aldgate', 'Angel', f'2023-10-{day:02d}')  # 2.00
    assert card.total() == 165.00  # Monthly cap reached

def test_unknown_station_origin():
    card = TransitFareCard()
    with pytest.raises(UnknownStation) as excinfo:
        card.journey('UnknownStation', 'Angel', '2023-10-01')
    assert str(excinfo.value) == "UnknownStation: UnknownStation"  # Journey from unknown station rejected

def test_unknown_station_destination():
    card = TransitFareCard()
    with pytest.raises(UnknownStation) as excinfo:
        card.journey('Aldgate', 'UnknownStation', '2023-10-01')
    assert str(excinfo.value) == "UnknownStation: UnknownStation"  # Journey to unknown station rejected

def test_rejected_journey_total_unchanged():
    card = TransitFareCard()
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    total_before = card.total()
    with pytest.raises(UnknownStation) as excinfo:
        card.journey('UnknownStation', 'Angel', '2023-10-01')  # Rejected
    assert str(excinfo.value) == "UnknownStation: UnknownStation"  # Journey rejected
    assert card.total() == total_before  # Total unchanged

def test_running_total():
    card = TransitFareCard()
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    assert card.total() == 5.50  # Total accumulated

def test_running_total_across_days():
    card = TransitFareCard()
    card.journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    card.journey('Aldgate', 'Angel', '2023-10-02')  # 2.50
    card.journey('Balham', 'Barbican', '2023-10-02')  # 3.00
    assert card.total() == 11.00  # Total across multiple days