import pytest
import random
from solution import reserve_machine, claim_machine

@pytest.fixture(autouse=True)
def reset_service():
    # Reset service state before each test
    pass  # Replace with actual service reset if needed

def test_reserve_machine_assigns_machine():
    # Reserve a machine; expect a machine number between 1 and 25 (inclusive)
    reservation = reserve_machine(user_id="user1", time_slot="2023-10-01T10:00:00", random=random.Random(1))
    assert 1 <= reservation['machine_number'] <= 25

def test_reserve_machine_generates_five_digit_pin():
    # Reserve a machine; expect a PIN of exactly five digits
    reservation = reserve_machine(user_id="user2", time_slot="2023-10-01T11:00:00", random=random.Random(2))
    assert len(reservation['pin']) == 5 and reservation['pin'].isdigit()

def test_reserve_machine_generates_unique_identifier():
    # Reserve a machine; expect an identifier of the form "RSV-" followed by 8 uppercase hex digits
    identifiers = set()
    for i in range(3):
        reservation = reserve_machine(user_id=f"user{i}", time_slot=f"2023-10-01T12:00:00", random=random.Random(i))
        assert reservation['identifier'].startswith("RSV-") and len(reservation['identifier']) == 12
        assert all(c in "0123456789ABCDEF" for c in reservation['identifier'][4:])
        identifiers.add(reservation['identifier'])
    assert len(identifiers) == 3  # Ensure no collision

def test_reserve_machine_starts_active():
    # Reserve a machine; expect the reservation to be active
    reservation = reserve_machine(user_id="user4", time_slot="2023-10-01T13:00:00", random=random.Random(4))
    assert reservation['active'] is True

def test_reserve_machine_records_time_slot():
    # Reserve a machine; expect the slot time to be recorded
    time_slot = "2023-10-01T14:00:00"
    reservation = reserve_machine(user_id="user5", time_slot=time_slot, random=random.Random(5))
    assert reservation['time_slot'] == time_slot

def test_reserve_machine_pin_distribution():
    # Reserve multiple machines to ensure PINs are drawn from the full five-digit range
    pins = {reserve_machine(user_id=f"user{i}", time_slot="2023-10-01T15:00:00", random=random.Random(i))['pin'] for i in range(1, 26)}
    assert len(pins) == 25  # Ensure we have 25 unique pins
    assert all(0 <= int(pin) < 100000 for pin in pins)  # Ensure all pins are five-digit

def test_reserve_machine_allocation_single_active():
    # Reserve a machine, then try to reserve another for the same user; expect an error
    reserve_machine(user_id="user6", time_slot="2023-10-01T16:00:00", random=random.Random(6))
    with pytest.raises(ReservationError) as excinfo:
        reserve_machine(user_id="user6", time_slot="2023-10-01T17:00:00", random=random.Random(7))
    assert str(excinfo.value) == "a user may only have a single active reservation at a time"

def test_reserve_machine_no_machines_available():
    # Reserve all machines and then try to reserve another; expect an error
    for i in range(1, 26):
        reserve_machine(user_id=f"user{i}", time_slot="2023-10-01T18:00:00", random=random.Random(i))
    with pytest.raises(ReservationError) as excinfo:
        reserve_machine(user_id="user26", time_slot="2023-10-01T19:00:00", random=random.Random(26))
    assert str(excinfo.value) == "no machines available"

def test_claim_machine_successful():
    # Reserve a machine, claim it with the correct PIN; expect successful claim
    reservation = reserve_machine(user_id="user7", time_slot="2023-10-01T20:00:00", random=random.Random(8))
    result = claim_machine(reservation['identifier'], reservation['pin'])
    assert result == "Claim accepted"  # Check acceptance message
    assert reservation['active'] is False  # Check reservation marked inactive

def test_claim_machine_incorrect_pin():
    # Reserve a machine, claim it with an incorrect PIN; expect failure
    reservation = reserve_machine(user_id="user8", time_slot="2023-10-01T21:00:00", random=random.Random(9))
    wrong_pin = str(int(reservation['pin']) + 1).zfill(5)  # Ensure wrong PIN
    result = claim_machine(reservation['identifier'], wrong_pin)
    assert result == "Claim rejected"  # Check rejection message
    assert reservation['active'] is True  # Reservation should still be active

def test_claim_machine_no_reservation():
    # Attempt to claim a machine with no reservation; expect rejection
    with pytest.raises(ClaimError) as excinfo:
        claim_machine("RSV-00000000", "12345")  # Guaranteed unreserved
    assert str(excinfo.value) == "No reservation found for this identifier"

def test_five_attempt_pin_reset():
    # Reserve a machine, enter wrong PIN four times, then correct it; expect no reset
    reservation = reserve_machine(user_id="user9", time_slot="2023-10-01T22:00:00", random=random.Random(10))
    for _ in range(4):
        claim_machine(reservation['identifier'], str(int(reservation['pin']) + 1).zfill(5))  # Wrong PIN
    result = claim_machine(reservation['identifier'], reservation['pin'])  # Correct PIN
    assert result == "Claim accepted"  # Check acceptance message
    assert reservation['active'] is False  # Reservation marked inactive

def test_pin_reset_on_fifth_failed_attempt():
    # Reserve a machine, enter wrong PIN five times; expect reset
    reservation = reserve_machine(user_id="user10", time_slot="2023-10-01T23:00:00", random=random.Random(11))
    old_pin = reservation['pin']
    for _ in range(5):
        claim_machine(reservation['identifier'], str(int(reservation['pin']) + 1).zfill(5))  # Wrong PIN
    assert reservation['pin'] != old_pin  # PIN should have changed
    assert reservation['active'] is True  # Still active after reset

def test_successful_claim_with_new_pin():
    # Reserve a machine, enter wrong PIN five times, then claim with new PIN; expect success
    reservation = reserve_machine(user_id="user11", time_slot="2023-10-01T24:00:00", random=random.Random(12))
    for _ in range(5):
        claim_machine(reservation['identifier'], str(int(reservation['pin']) + 1).zfill(5))  # Wrong PIN
    new_result = claim_machine(reservation['identifier'], reservation['pin'])  # Try with new PIN
    assert new_result == "Claim accepted"  # Check acceptance message
    assert reservation['active'] is False  # Reservation marked inactive