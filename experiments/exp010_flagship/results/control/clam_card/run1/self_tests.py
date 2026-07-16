from solution import TransitCard

def test_journey_within_zone_a():
    card = TransitCard()
    amount = card.take_journey('Aldgate', 'Anerley', '2023-10-01')
    assert amount == 2.50  # Journey wholly within Zone A costs 2.50
    assert card.get_total() == 2.50  # Running total should reflect this charge

def test_journey_wholly_within_zone_b():
    card = TransitCard()
    amount = card.take_journey('Balham', 'Barbican', '2023-10-01')
    assert amount == 3.00  # Journey wholly within Zone B costs 3.00
    assert card.get_total() == 3.00  # Running total should reflect this charge

def test_journey_touching_zone_b():
    card = TransitCard()
    amount = card.take_journey('Aldgate', 'Balham', '2023-10-01')
    assert amount == 3.00  # Journey touching Zone B costs 3.00
    assert card.get_total() == 3.00  # Running total should reflect this charge

def test_daily_cap_zone_a():
    card = TransitCard()
    card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.take_journey('Aldgate', 'Angel', '2023-10-01')    # 2.50
    card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.00
    amount = card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 0.00
    assert amount == 0.00  # Daily cap reached at 7.00
    assert card.get_total() == 7.00  # Total should be capped at 7.00

def test_daily_cap_zone_b():
    card = TransitCard()
    card.take_journey('Balham', 'Barbican', '2023-10-01')  # 3.00
    card.take_journey('Balham', 'Bison', '2023-10-01')     # 3.00
    amount = card.take_journey('Balham', 'Bugel', '2023-10-01')  # 2.00
    assert amount == 2.00  # Daily cap reached at 8.00
    assert card.get_total() == 8.00  # Total should be capped at 8.00

def test_zone_b_journey_after_zone_a_cap():
    card = TransitCard()
    card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
    card.take_journey('Aldgate', 'Angel', '2023-10-01')    # 2.50
    card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.00
    card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 0.00
    amount = card.take_journey('Aldgate', 'Balham', '2023-10-01')  # 1.00
    assert amount == 1.00  # Cap lifted to Zone B, charges 1.00 difference
    assert card.get_total() == 8.00  # Total should reflect Zone B cap

def test_weekly_cap_zone_a():
    card = TransitCard()
    for _ in range(3):
        card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
        card.take_journey('Aldgate', 'Angel', '2023-10-01')    # 2.50
    for _ in range(3):
        card.take_journey('Aldgate', 'Anerley', '2023-10-02')  # 2.50
        card.take_journey('Aldgate', 'Angel', '2023-10-02')    # 2.50
    amount = card.take_journey('Aldgate', 'Anerley', '2023-10-02')  # 0.00
    assert amount == 0.00  # Weekly cap reached at 40.00
    assert card.get_total() == 40.00  # Total should be capped at 40.00

def test_monthly_cap_zone_a():
    card = TransitCard()
    for _ in range(3):
        card.take_journey('Aldgate', 'Anerley', '2023-10-01')  # 2.50
        card.take_journey('Aldgate', 'Angel', '2023-10-01')    # 2.50
    
    # Assuming 30 days in the month and 3 journeys a day
    for day in range(30):
        for _ in range(3):
            card.take_journey('Aldgate', 'Anerley', f'2023-10-{day + 1:02d}')  # 2.50
            card.take_journey('Aldgate', 'Angel', f'2023-10-{day + 1:02d}')    # 2.50
    
    assert card.get_total() == 145.00  # Total should be capped at 145.00

def test_unknown_station_rejected():
    card = TransitCard()
    amount = card.take_journey('Aldgate', 'UnknownStation', '2023-10-01')
    assert amount == 'unknown-station: UnknownStation'  # Journey should be rejected
    assert card.get_total() == 0.00  # Total should remain unchanged

def test_double_unknown_station_rejected():
    card = TransitCard()
    card.take_journey('Aldgate', 'UnknownStation', '2023-10-01')
    amount = card.take_journey('UnknownStation', 'Anerley', '2023-10-01')
    assert amount == 'unknown-station: UnknownStation'  # Both journeys should be rejected
    assert card.get_total() == 0.00  # Total should remain unchanged

def test_running_total_no_charge():
    card = TransitCard()
    card.take_journey('Aldgate', 'UnknownStation', '2023-10-01')  # Journey rejected
    assert card.get_total() == 0.00  # Total should remain unchanged