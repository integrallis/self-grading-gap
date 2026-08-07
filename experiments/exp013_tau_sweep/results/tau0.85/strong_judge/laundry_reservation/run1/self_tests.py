import pytest
from solution import reserve_machine, claim_machine
import random

def seeded_random(seed):
    """ Create a random source with a given seed. """
    rng = random.Random(seed)
    return rng

@pytest.fixture(autouse=True)
def reset_service():
    """ Reset service state for each test. """
    pass  # Placeholder for service state reset logic

def test_reserve_machine_success():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, cell_phone, time_slot)
    
    # Check the machine number is between 1 and 25
    assert 1 <= reservation['machine_number'] <= 25
    
    # Check PIN is exactly five digits
    assert len(reservation['pin']) == 5
    assert reservation['pin'].isdigit()
    
    # Check identifier is of the form "RSV-" followed by eight uppercase hex digits
    assert reservation['identifier'].startswith("RSV-")
    assert len(reservation['identifier']) == 12  # 4 + 8
    assert all(c in "0123456789ABCDEF" for c in reservation['identifier'][4:])

    # Check reservation is active
    assert reservation['active'] is True
    
    # Check the requested slot time is recorded
    assert reservation['slot_time'] == time_slot

def test_reserve_machine_unique_identifiers():
    random_source1 = seeded_random(1)
    random_source2 = seeded_random(2)
    email1 = "resident1@example.com"
    email2 = "resident2@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation1 = reserve_machine(random_source1, email1, cell_phone, time_slot)
    reservation2 = reserve_machine(random_source2, email2, cell_phone, time_slot)

    # Check that identifiers are unique
    assert reservation1['identifier'] != reservation2['identifier']

def test_reserve_machine_single_reservation():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot1 = "2023-10-01T10:00:00"
    time_slot2 = "2023-10-01T11:00:00"

    reserve_machine(random_source, email, cell_phone, time_slot1)
    
    # Attempt to reserve again should raise a reservation error
    with pytest.raises(Exception, match="^a user may only have a single active reservation at a time$"):
        reserve_machine(random_source, email, cell_phone, time_slot2)

def test_reserve_machine_no_machines_available():
    random_source = seeded_random(1)
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    # Reserve all machines
    for i in range(25):
        reserve_machine(random_source, f"resident{i}@example.com", cell_phone, time_slot)
    
    # Attempt to reserve another machine should raise a reservation error
    with pytest.raises(Exception, match="^no machines available$"):
        reserve_machine(random_source, "resident@example.com", cell_phone, time_slot)

def test_claim_machine_success():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, cell_phone, time_slot)
    pin = reservation['pin']
    
    # Claim the machine with the correct PIN
    claim_result = claim_machine(reservation['identifier'], pin)
    
    # Check that the claim was accepted
    assert claim_result['accepted'] is True
    # Check the reservation is marked used (assuming there's a way to check this)
    assert not reservation['active']  # This assumes the reservation object mutates

def test_claim_machine_wrong_pin():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, cell_phone, time_slot)
    wrong_pin = str(int(reservation['pin']) + 1).zfill(5)  # Ensure this is a different PIN
    
    # Attempt to claim the machine with the wrong PIN
    claim_result = claim_machine(reservation['identifier'], wrong_pin)
    
    # Check that the claim was rejected and the reservation remains active
    assert claim_result['accepted'] is False
    assert reservation['active'] is True  # Reservation should still be active

def test_claim_machine_no_reservation():
    random_source = seeded_random(1)
    wrong_identifier = "RSV-00000000"  # No such reservation
    
    # Attempt to claim the machine with no reservation
    claim_result = claim_machine(wrong_identifier, "12345")
    assert claim_result['accepted'] is False  # Assuming this indicates a rejection

def test_five_attempt_pin_reset():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, cell_phone, time_slot)
    
    # Simulate four failed attempts
    for _ in range(4):
        claim_machine(reservation['identifier'], "wrong_pin")
    
    # The fifth attempt should trigger a reset
    new_claim_result = claim_machine(reservation['identifier'], "wrong_pin")
    
    # Check that the claim was rejected
    assert new_claim_result['accepted'] is False
    # Here we would need to check if a new PIN is generated and a text message sent
    # These checks are assumed and would depend on the API's design

def test_claim_machine_after_reset():
    random_source = seeded_random(1)
    email = "resident@example.com"
    cell_phone = "1234567890"
    time_slot = "2023-10-01T10:00:00"
    
    reservation = reserve_machine(random_source, email, cell_phone, time_slot)
    
    # Simulate four failed attempts
    for _ in range(4):
        claim_machine(reservation['identifier'], "wrong_pin")
    
    # The fifth attempt should reset the PIN
    claim_machine(reservation['identifier'], "wrong_pin")

    # Now, claim the machine with the new PIN (assuming we can retrieve it)
    # We would need a way to capture the new PIN generated
    new_pin = "new_generated_pin"  # Placeholder for the new PIN
    claim_result = claim_machine(reservation['identifier'], new_pin)  
    assert claim_result['accepted'] is True