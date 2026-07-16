import pytest
from solution import reserve_machine, claim_machine, reset_pin

def test_reserve_machine_success():
    # Assuming the randomness source is seeded to produce a specific machine, PIN, and ID
    random_source = seed_random_source(123)  # Example seed
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, time_slot)
    
    # AC-1.1: Machine number between 1 and 25
    assert 1 <= reservation.machine_number <= 25
    
    # AC-1.2: PIN is exactly 5 digits
    assert len(reservation.pin) == 5
    
    # AC-1.3: Identifier format is RSV- followed by 8 uppercase hex digits
    assert reservation.identifier.startswith("RSV-")
    assert len(reservation.identifier) == 12  # 4 + 8
    assert all(c in "0123456789ABCDEF" for c in reservation.identifier[4:])
    
    # AC-1.4: Reservation is active and can be looked up by its identifier
    assert reservation.is_active
    
    # AC-1.5: Slot date and time are accurately recorded
    assert reservation.slot_time == time_slot
    
    # AC-1.6: PINs are drawn from the full five-digit range
    assert 10000 <= int(reservation.pin) <= 99999
    
    # AC-1.7: Same random source produces identical reservations
    second_reservation = reserve_machine(random_source, email, time_slot)
    assert reservation == second_reservation

def test_reserve_machine_second_active_reservation():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reserve_machine(random_source, email, time_slot)  # First reservation
    
    with pytest.raises(Exception) as excinfo:
        reserve_machine(random_source, email, time_slot)  # Second reservation attempt
    assert str(excinfo.value) == "a user may only have a single active reservation at a time"

def test_reserve_machine_no_machines_available():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    
    # Reserve all machines
    for i in range(25):
        reserve_machine(random_source, email, f"2023-10-01T10:00:00")
    
    with pytest.raises(Exception) as excinfo:
        reserve_machine(random_source, email, "2023-10-01T10:00:00")  # No machines available
    assert str(excinfo.value) == "no machines available"

def test_claim_machine_success():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, time_slot)
    
    claim_result = claim_machine(reservation.identifier, reservation.pin)
    
    # AC-4.1: Claim succeeds
    assert claim_result.success
    
    # AC-4.2: Machine is unlocked
    assert claim_result.machine_unlocked
    
    # AC-4.5: Reservation is no longer active
    assert not reservation.is_active

def test_claim_machine_wrong_pin():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, time_slot)
    
    claim_result = claim_machine(reservation.identifier, "wrong_pin")
    
    # AC-4.3: Wrong PIN rejected
    assert not claim_result.success
    
    # Reservation still active
    assert reservation.is_active

def test_claim_machine_no_reservation():
    with pytest.raises(Exception) as excinfo:
        claim_machine("RSV-00000000", "12345")  # No reservation exists
    assert str(excinfo.value) == "Claiming a machine that has no reservation is rejected"
    
def test_five_attempt_pin_reset():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, time_slot)
    
    # Simulate 4 wrong attempts
    for _ in range(4):
        claim_machine(reservation.identifier, "wrong_pin")

    # Fifth attempt should trigger reset
    new_pin = reset_pin(reservation.identifier)
    
    # AC-5.2: New PIN sent to resident's phone
    assert new_pin != reservation.pin  # Ensure it's a new PIN
    
    # AC-5.4: Regenerated PIN accepted for claiming
    claim_result = claim_machine(reservation.identifier, new_pin)
    assert claim_result.success

def test_pin_reset_restarts_attempt_count():
    random_source = seed_random_source(123)
    email = "resident@example.com"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, time_slot)
    
    # Simulate 4 wrong attempts
    for _ in range(4):
        claim_machine(reservation.identifier, "wrong_pin")

    # Fifth attempt should trigger reset
    new_pin = reset_pin(reservation.identifier)

    # Try wrong PIN again up to 4 more times
    for _ in range(4):
        claim_machine(reservation.identifier, "wrong_pin")

    # Fifth attempt should trigger a new reset
    new_pin_again = reset_pin(reservation.identifier)
    assert new_pin_again != new_pin  # Ensure it's a new PIN