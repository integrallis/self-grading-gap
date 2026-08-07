import pytest
from solution import reserve_machine, claim_machine

def test_reserve_machine_success():
    # Given a source of randomness
    import random
    random_source = random.Random(42)  # Create a random source with a fixed seed
    
    # When reserving a machine for a time slot
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random_source)
    
    # Then a machine is assigned (1 <= machine_number <= 25)
    assert 1 <= reservation['machine_number'] <= 25
    # And a 5-digit PIN is generated
    assert len(reservation['pin']) == 5
    assert all("0" <= c <= "9" for c in reservation['pin'])  # Check if PIN contains only ASCII digits
    # And an identifier is generated
    assert reservation['identifier'].startswith("RSV-")
    assert len(reservation['identifier']) == 12  # "RSV-" + 8 hex digits
    assert all(c in '0123456789ABCDEF' for c in reservation['identifier'][4:])  # Check hex digits
    # And the reservation is active
    assert reservation['active'] is True
    # And the correct time slot is recorded
    assert reservation['time_slot'] == "2023-10-01T10:00:00"

def test_reserve_machine_user_limit():
    # Given a source of randomness
    import random
    random_source = random.Random(42)
    
    # When reserving the first machine
    reservation1 = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random_source)
    
    # When reserving a second machine
    with pytest.raises(Exception) as excinfo:
        reserve_machine("user@example.com", "123-456-7890", "2023-10-01T11:00:00", random_source)
    assert str(excinfo.value) == "a user may only have a single active reservation at a time"

def test_reserve_machine_no_machines_available():
    # Given a source of randomness
    import random
    random_source = random.Random(42)
    
    # Reserve all machines (25)
    for i in range(25):
        reserve_machine(f"user{i}@example.com", "123-456-7890", f"2023-10-01T{i:02}:00:00", random_source)
    
    # When trying to reserve one more machine
    with pytest.raises(Exception) as excinfo:
        reserve_machine("user26@example.com", "123-456-7890", "2023-10-01T12:00:00", random_source)
    assert str(excinfo.value) == "no machines available"

def test_claim_machine_success():
    # Given a successful reservation
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random.Random(42))
    
    # When claiming the machine with the correct PIN
    claim_result = claim_machine(reservation['identifier'], reservation['pin'])
    
    # Then claiming succeeds
    assert claim_result['success'] is True
    # And the reservation can be looked up by identifier to verify it is no longer active
    updated_reservation = claim_machine(reservation['identifier'], "")
    assert updated_reservation['active'] is False

def test_claim_machine_wrong_pin():
    # Given a successful reservation
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random.Random(42))
    
    # When claiming the machine with a wrong PIN
    wrong_pin = "00000" if reservation['pin'] != "00000" else "00001"
    claim_result = claim_machine(reservation['identifier'], wrong_pin)
    
    # Then claiming fails
    assert claim_result['success'] is False
    # And the reservation remains active
    updated_reservation = claim_machine(reservation['identifier'], "")
    assert updated_reservation['active'] is True

def test_five_attempt_pin_reset():
    # Given a successful reservation
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random.Random(42))
    
    # Save the original PIN for comparison
    original_pin = reservation['pin']
    
    # Simulate 4 failed attempts
    for _ in range(4):
        claim_result = claim_machine(reservation['identifier'], "00000" if original_pin != "00000" else "00001")
        assert claim_result['success'] is False
        assert reservation['pin'] == original_pin  # PIN remains unchanged
    
    # On the fifth failed attempt
    claim_result = claim_machine(reservation['identifier'], "00000" if original_pin != "00000" else "00001")
    assert claim_result['success'] is False
    # And the PIN should be reset
    assert reservation['pin'] != original_pin  # New PIN generated
    # Here, we would check if a text message was sent, which is not implemented in this test.

def test_unique_identifiers():
    # Given a source of randomness
    import random
    random_source = random.Random(42)
    
    identifiers = set()
    
    # Create multiple reservations for uniqueness test
    for i in range(25):
        reservation = reserve_machine(f"user{i}@example.com", "123-456-7890", f"2023-10-01T{i:02}:00:00", random_source)
        identifiers.add(reservation['identifier'])
    
    # Assert all identifiers are distinct
    assert len(identifiers) == 25  # Each identifier must be unique

def test_successful_claim_unlocks_machine():
    # Given a successful reservation
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random.Random(42))
    
    # When claiming the machine with the correct PIN
    claim_result = claim_machine(reservation['identifier'], reservation['pin'])
    
    # Then the machine should be unlocked
    assert claim_result['machine_unlocked'] is True  # Assuming this is part of the claim response

def test_no_reservation_claim_rejected():
    # Given a non-existent reservation
    with pytest.raises(Exception) as excinfo:
        claim_machine("RSV-00000000", "12345")  # Claiming a non-existent identifier
    assert str(excinfo.value) == "No reservation found for this identifier"

def test_reserve_again_after_claim():
    # Given a successful reservation
    reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T10:00:00", random.Random(42))
    
    # When claiming the machine
    claim_machine(reservation['identifier'], reservation['pin'])
    
    # Then the user should be able to reserve again
    new_reservation = reserve_machine("user@example.com", "123-456-7890", "2023-10-01T11:00:00", random.Random(42))
    assert new_reservation['identifier'] != reservation['identifier']  # New identifier generated