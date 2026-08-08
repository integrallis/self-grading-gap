import random
import string
import pytest
import re
from solution import reserve_machine, claim_machine

# Helper to generate a random reservation identifier
def generate_identifier():
    return "RSV-" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

# Helper to generate a random 5-digit PIN
def generate_pin():
    return str(random.randint(0, 99999)).zfill(5)

# Test for reserving a machine successfully
def test_reserve_machine_success():
    # Given a resident wants to reserve a machine
    resident_email = "resident@example.com"
    resident_phone = "1234567890"
    time_slot = "2023-10-10T10:00:00"

    # When reserving a machine
    machine_number, pin, identifier = reserve_machine(resident_email, resident_phone, time_slot)

    # Then a machine number between 1 and 25 is assigned
    assert 1 <= machine_number <= 25

    # And the PIN is exactly five digits
    assert len(pin) == 5 and pin.isdigit()

    # And the identifier is in the correct format
    assert re.fullmatch(r"RSV-[0-9A-F]{8}", identifier)

    # And the reservation is active (this check should be done by a proper reservation lookup)
    # Assuming a way to lookup by identifier
    reservation = claim_machine(identifier, pin)  # This function isn't defined but serves as a placeholder
    assert reservation.is_active  # Check if reservation is active

    # And the slot date and time matches the requested time
    assert reservation.slot == time_slot

# Test for concurrent reservations
def test_reserve_machine_concurrent_reservations():
    resident_email = "resident@example.com"
    resident_phone = "1234567890"
    time_slot = "2023-10-10T10:00:00"

    # Reserve the first machine
    reserve_machine(resident_email, resident_phone, time_slot)

    # When trying to reserve again
    with pytest.raises(Exception) as error_info:  # Use general exception as we do not know the exact type
        reserve_machine(resident_email, resident_phone, time_slot)
    assert str(error_info.value) == "a user may only have a single active reservation at a time"

# Test for no machines available
def test_reservation_no_machines_available():
    for i in range(25):
        resident_email = f"resident{i}@example.com"
        resident_phone = "1234567890"
        time_slot = f"2023-10-10T10:00:00"
        reserve_machine(resident_email, resident_phone, time_slot)

    # When trying to reserve another machine
    with pytest.raises(Exception) as error_info:  # Use general exception as we do not know the exact type
        reserve_machine("new_resident@example.com", "1234567890", "2023-10-10T10:00:00")
    assert str(error_info.value) == "no machines available"

# Test for claiming the machine with correct PIN
def test_claim_machine_with_correct_pin():
    resident_email = "resident@example.com"
    resident_phone = "1234567890"
    time_slot = "2023-10-10T10:00:00"

    # Reserve a machine
    machine_number, pin, identifier = reserve_machine(resident_email, resident_phone, time_slot)

    # When claiming the machine with the correct PIN
    assert claim_machine(identifier, pin)  # Assume that this returns True if successful

    # And the reservation is marked as used (this check should be done by a proper reservation lookup)
    reservation = claim_machine(identifier, pin)  # This function isn't defined but serves as a placeholder
    assert not reservation.is_active

# Test for claiming the machine with wrong PIN
def test_claim_machine_with_wrong_pin():
    resident_email = "resident@example.com"
    resident_phone = "1234567890"
    time_slot = "2023-10-10T10:00:00"

    # Reserve a machine
    machine_number, pin, identifier = reserve_machine(resident_email, resident_phone, time_slot)

    # Prepare a wrong PIN
    wrong_pin = "00000" if pin != "00000" else "00001"

    # When claiming the machine with the wrong PIN
    assert not claim_machine(identifier, wrong_pin)  # Assume this returns False

    # And the reservation stays active (this check should be done by a proper reservation lookup)
    reservation = claim_machine(identifier, pin)  # This function isn't defined but serves as a placeholder
    assert reservation.is_active

# Test for claiming a machine that has no reservation
def test_claim_machine_no_reservation():
    # When trying to claim a machine with no reservation
    assert not claim_machine("RSV-XXXXXXXX", "12345")  # Assuming it just returns False without raising

# Test for PIN reset after five failed attempts
def test_pin_reset_after_five_failed_attempts():
    resident_email = "resident@example.com"
    resident_phone = "1234567890"
    time_slot = "2023-10-10T10:00:00"

    # Reserve a machine
    machine_number, pin, identifier = reserve_machine(resident_email, resident_phone, time_slot)

    # Simulate four failed attempts
    for _ in range(4):
        assert not claim_machine(identifier, "00000")  # Wrong PIN

    # When the fifth wrong attempt is made
    assert not claim_machine(identifier, "00000")  # This should trigger a reset

    # Then the new PIN is generated and sent to the resident via SMS (not checked here)
    # Assuming we can check the new PIN from some kind of lookup
    new_pin = claim_machine(identifier, "00000")  # This function isn't defined but serves as a placeholder

    # And the machine is still claimed with the new PIN
    assert claim_machine(identifier, new_pin)  # Assume this returns True