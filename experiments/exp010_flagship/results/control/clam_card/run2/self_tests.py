from solution import TransitCard

def test_zone_a_whole_journey():
    card = TransitCard()
    charge = card.add_journey('Aldgate', 'Angel', '2023-10-01')  # Journey within Zone A
    assert charge == 2.50  # AC-1.1
    assert card.get_total() == 2.50  # AC-5.1

def test_zone_b_whole_journey():
    card = TransitCard()
    charge = card.add_journey('Balham', 'Barbican', '2023-10-01')  # Journey within Zone B
    assert charge == 3.00  # AC-1.2
    assert card.get_total() == 3.00  # AC-5.1

def test_zone_a_to_zone_b_journey():
    card = TransitCard()
    charge = card.add_journey('Aldgate', 'Balham', '2023-10-01')  # Journey touching Zone B
    assert charge == 3.00  # AC-1.2
    assert card.get_total() == 3.00  # AC-5.1

def test_multiple_zone_a_journeys_daily_cap():
    card = TransitCard()
    card.add_journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.add_journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    charge = card.add_journey('Aldgate', 'Angel', '2023-10-01')  # 2.00 (capped)
    assert charge == 2.00  # AC-2.1
    assert card.get_total() == 7.00  # AC-5.1

def test_zone_b_journeys_daily_cap():
    card = TransitCard()
    card.add_journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    card.add_journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    charge = card.add_journey('Balham', 'Barbican', '2023-10-01')  # 2.00 (capped)
    assert charge == 2.00  # AC-2.2
    assert card.get_total() == 8.00  # AC-5.1

def test_zone_a_and_zone_b_journey_daily_cap():
    card = TransitCard()
    card.add_journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.add_journey('Aldgate', 'Angel', '2023-10-01')  # 2.50
    card.add_journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    charge = card.add_journey('Balham', 'Barbican', '2023-10-01')  # 1.00 (lift cap to Zone B)
    assert charge == 1.00  # AC-2.4
    assert card.get_total() == 8.00  # AC-5.1

def test_weekly_cap_zone_a():
    card = TransitCard()
    for _ in range(3):  # 3 journeys per day for 6 days
        card.add_journey('Aldgate', 'Angel', '2023-10-01')
        card.add_journey('Aldgate', 'Angel', '2023-10-02')
        card.add_journey('Aldgate', 'Angel', '2023-10-03')
    assert card.get_total() == 40.00  # AC-3.1

def test_monthly_cap_zone_a():
    card = TransitCard()
    for _ in range(3):  # 3 journeys per day for 30 days
        card.add_journey('Aldgate', 'Angel', '2023-10-01')
    assert card.get_total() == 145.00  # AC-3.3

def test_unknown_station_journey():
    card = TransitCard()
    charge = card.add_journey('Unknown', 'Aldgate', '2023-10-01')  # Journey from unknown station
    assert charge is None  # AC-4.1
    assert card.get_total() == 0.00  # AC-4.2

def test_reject_journey_to_unknown_station():
    card = TransitCard()
    charge = card.add_journey('Aldgate', 'Unknown', '2023-10-01')  # Journey to unknown station
    assert charge is None  # AC-4.1
    assert card.get_total() == 0.00  # AC-4.2