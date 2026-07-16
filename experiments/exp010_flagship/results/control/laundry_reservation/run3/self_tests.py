from solution import reserve_machine, claim_machine, reset_pin

def test_reserve_machine_success():
    # Assuming a random source that generates the following:
    # Machine number: 1 (valid)
    # PIN: 12345 (valid 5-digit)
    # Identifier: RSV-12345678 (valid non-empty identifier of 16 characters)
    # Slot time: "2023-10-10T10:00:00"
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    assert reservation.machine_number == 1
    assert reservation.pin == 12345
    assert reservation.identifier.startswith("RSV-") and len(reservation.identifier) == 16  # "RSV-" + 8 hex digits
    assert reservation.is_active is True
    assert reservation.slot_time == "2023-10-10T10:00:00"

def test_reserve_machine_pin_length():
    # Check that the PIN is exactly 5 digits
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    assert len(str(reservation.pin)) == 5

def test_reserve_machine_identifier_format():
    # Check that the identifier is in the correct format
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    assert reservation.identifier.startswith("RSV-") and len(reservation.identifier) == 16  # "RSV-" + 8 hex digits

def test_reserve_machine_single_active_reservation():
    reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    with pytest.raises(ReservationError, match="a user may only have a single active reservation at a time"):
        reserve_machine(random_source, "user@example.com", "2023-10-10T11:00:00")

def test_reserve_machine_no_machines_available():
    # Assume all machines are reserved
    reserve_all_machines()
    with pytest.raises(ReservationError, match="no machines available"):
        reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")

def test_claim_machine_success():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    assert claim_machine(reservation.identifier, reservation.pin) is True
    assert reservation.is_active is False

def test_claim_machine_wrong_pin():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    assert claim_machine(reservation.identifier, "wrong-pin") is False
    assert reservation.is_active is True

def test_claim_machine_no_reservation():
    assert claim_machine("no-such-id", "12345") is False

def test_claim_machine_already_used():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    claim_machine(reservation.identifier, reservation.pin)
    assert claim_machine(reservation.identifier, reservation.pin) is False

def test_reset_pin_success():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    for _ in range(4):  # Simulate 4 failed attempts
        claim_machine(reservation.identifier, "wrong-pin")
    assert reset_pin(reservation.identifier) is True
    assert reservation.pin != "previous-pin-placeholder"  # Replace with the actual previous PIN for validation
    assert text_message_sent_to("user@example.com", reservation.pin)

def test_reset_pin_fifth_attempt():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    for _ in range(5):  # Simulate 5 failed attempts
        claim_machine(reservation.identifier, "wrong-pin")
    assert reset_pin(reservation.identifier) is True
    assert text_message_sent_to("user@example.com", reservation.pin)

def test_reset_pin_failed_attempt_count_resets():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    for _ in range(4): 
        claim_machine(reservation.identifier, "wrong-pin")
    reset_pin(reservation.identifier)
    for _ in range(4): 
        claim_machine(reservation.identifier, "wrong-pin")
    assert reset_pin(reservation.identifier) is True

def test_reset_pin_successive_attempts():
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-10T10:00:00")
    for _ in range(5):
        claim_machine(reservation.identifier, "wrong-pin")
    assert reset_pin(reservation.identifier) is True
    # Check that the new pin is accepted
    assert claim_machine(reservation.identifier, reservation.pin) is True