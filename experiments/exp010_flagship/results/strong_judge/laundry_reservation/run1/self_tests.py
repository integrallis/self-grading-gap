import pytest
from solution import reserve_machine, claim_machine

@pytest.fixture
def create_reservation_service():
    class ReservationService:
        def __init__(self, seed):
            self.seed = seed
            # Initialize the service with a deterministic random source using the seed

        def create_reservation(self, email, phone, slot_time):
            return reserve_machine(email, phone, slot_time, self.seed)

    return ReservationService

def test_reserve_machine_assigns_machine(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    assert 1 <= reservation['machine_number'] <= 25

def test_reserve_machine_generates_pin(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    assert len(reservation['pin']) == 5
    assert reservation['pin'].isdigit()

def test_reserve_machine_generates_identifier(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    assert reservation['identifier'].startswith("RSV-")
    assert len(reservation['identifier']) == 12  # "RSV-" + 8 hex digits
    assert all(c in "0123456789ABCDEF" for c in reservation['identifier'][4:])

def test_reserve_machine_starts_active(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    assert reservation['active'] is True

def test_reserve_machine_records_slot_time(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    assert reservation['slot_time'] == 10

def test_reserve_machine_pin_range(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation1 = service.create_reservation("user1@example.com", "123-456-7890", 10)
    reservation2 = service.create_reservation("user2@example.com", "123-456-7890", 12)
    assert 0 <= int(reservation1['pin']) <= 99999
    assert 0 <= int(reservation2['pin']) <= 99999

def test_reserve_machine_respects_random_seed(create_reservation_service):
    service1 = create_reservation_service(seed=1)
    service2 = create_reservation_service(seed=1)
    reservation1 = service1.create_reservation("user@example.com", "123-456-7890", 10)
    reservation2 = service2.create_reservation("user@example.com", "123-456-7890", 10)
    assert reservation1 == reservation2

def test_reserve_machine_sends_confirmation_email(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    # Simulate checking the email content (this is a placeholder for the actual email check)
    assert reservation.get('confirmation_email') == {
        'to': "user@example.com",
        'machine_number': reservation['machine_number'],
        'identifier': reservation['identifier'],
        'pin': reservation['pin']
    }

def test_reserve_machine_locks_machine(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    # Simulate checking if the correct machine lock engagement occurred (this is a placeholder)
    assert reservation.get('machine_locked') == True

def test_single_active_reservation(create_reservation_service):
    service = create_reservation_service(seed=1)
    service.create_reservation("user@example.com", "123-456-7890", 10)
    with pytest.raises(Exception) as excinfo:
        service.create_reservation("user@example.com", "123-456-7890", 12)
    assert str(excinfo.value) == "a user may only have a single active reservation at a time"

def test_no_machines_available(create_reservation_service):
    service = create_reservation_service(seed=1)
    for i in range(1, 26):
        service.create_reservation(f"user{i}@example.com", "123-456-7890", 10)
    with pytest.raises(Exception) as excinfo:
        service.create_reservation("user27@example.com", "123-456-7890", 10)
    assert str(excinfo.value) == "no machines available"

def test_claim_machine_success(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    result = claim_machine(reservation['identifier'], reservation['pin'])
    assert result == "accepted"  # assuming the result indicates success

def test_claim_machine_wrong_pin(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    wrong_pin = str(int(reservation['pin']) + 1).zfill(5)  # Generate a wrong PIN
    result = claim_machine(reservation['identifier'], wrong_pin)
    assert result == "rejected"  # assuming the result indicates failure
    assert reservation['active'] is True

def test_claim_machine_no_reservation():
    with pytest.raises(Exception) as excinfo:
        claim_machine("RSV-00000000", "12345")
    assert str(excinfo.value) == "claiming a machine that has no reservation is rejected"

def test_claim_machine_already_used(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    claim_machine(reservation['identifier'], reservation['pin'])
    result = claim_machine(reservation['identifier'], reservation['pin'])
    assert result == "rejected"  # assuming the result indicates failure

def test_five_attempts_pin_reset_no_message(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    for _ in range(4):
        claim_machine(reservation['identifier'], "99999")  # Using an invalid pin
    # No message should be sent yet (assumed behavior)
    assert reservation.get('pin_reset_message_sent') is False

def test_fifth_attempt_pin_reset(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    for _ in range(5):
        claim_machine(reservation['identifier'], "99999")  # Using an invalid pin
    # Check that a message has been sent
    assert reservation.get('pin_reset_message_sent') is True

def test_reset_pin_reengages_machine_lock(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    for _ in range(5):
        claim_machine(reservation['identifier'], "99999")  # Using an invalid pin
    # Check if the machine was re-engaged with the new pin
    assert reservation.get('machine_locked') is True

def test_reset_pin_accepts_new_pin(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    for _ in range(5):
        claim_machine(reservation['identifier'], "99999")  # Using an invalid pin
    # Assuming the new pin is now available
    assert claim_machine(reservation['identifier'], reservation['pin']) == "accepted"  # Replace with actual pin logic

def test_failed_attempt_count_resets_after_reset(create_reservation_service):
    service = create_reservation_service(seed=1)
    reservation = service.create_reservation("user@example.com", "123-456-7890", 10)
    for _ in range(5):
        claim_machine(reservation['identifier'], "99999")  # Using an invalid pin
    # Next fresh attempts should be counted separately
    result = claim_machine(reservation['identifier'], "99999")  # Using the same wrong pin
    assert result == "rejected"
    result = claim_machine(reservation['identifier'], "99999")
    assert result == "rejected"
    result = claim_machine(reservation['identifier'], "99999")
    assert result == "rejected"
    result = claim_machine(reservation['identifier'], "99999")
    assert result == "rejected"
    result = claim_machine(reservation['identifier'], "99999")
    assert result == "rejected"