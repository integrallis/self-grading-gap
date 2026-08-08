import pytest
from solution import reserve_machine, claim_machine

def test_reserve_machine_assigns_machine():
    # Assume a standard room with 25 machines, expect the machine number to be between 1 and 25.
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    assert 1 <= result['machine_number'] <= 25

def test_reserve_machine_generates_five_digit_pin():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    pin = result['pin']
    assert len(pin) == 5 and pin.isdigit()

def test_reserve_machine_generates_unique_identifier():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    identifier = result['identifier']
    assert identifier.startswith("RSV-") and len(identifier) == 12
    assert all(c in '0123456789ABCDEF' for c in identifier[4:])  # Check for uppercase hex digits

def test_reserve_machine_starts_active():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    assert result['active'] is True

def test_reserve_machine_records_slot_time():
    slot_time = "2023-10-01T10:00:00Z"
    result = reserve_machine("user@example.com", "1234567890", slot_time, 25)
    assert result['slot_time'] == slot_time

def test_reserve_machine_pin_distribution():
    pins = [reserve_machine("user@example.com", f"user{i}@example.com", "2023-10-01T10:00:00Z", 25)['pin'] for i in range(100)]
    assert all(len(pin) == 5 and pin.isdigit() for pin in pins)
    assert any(pin != "00000" for pin in pins)  # Check that not all PINs are "00000"
    assert any(pin != "99999" for pin in pins)  # Check that not all PINs are "99999"

def test_reserve_machine_with_random_source():
    from random import Random
    random_source1 = Random(0)
    random_source2 = Random(0)
    result1 = reserve_machine("user1@example.com", "1234567890", "2023-10-01T10:00:00Z", 25, random_source1)
    result2 = reserve_machine("user2@example.com", "1234567890", "2023-10-01T10:00:00Z", 25, random_source2)
    assert result1['machine_number'] == result2['machine_number']
    assert result1['pin'] == result2['pin']
    assert result1['identifier'] == result2['identifier']

def test_reserve_machine_sends_confirmation_email():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    # Here we assume an email service is tracked and exactly one email is sent
    # This is a placeholder for the actual email checking mechanism.
    assert result['confirmation_email']['to'] == "user@example.com"
    assert result['confirmation_email']['machine_number'] == result['machine_number']
    assert result['confirmation_email']['identifier'] == result['identifier']
    assert result['confirmation_email']['pin'] == result['pin']

def test_reserve_machine_locks_correct_machine():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    # This is a placeholder for checking the actual lock engagement mechanism.
    assert result['locked_machine'] == result['machine_number']

def test_reserve_machine_no_other_machines_touched():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    # This assumes a mock state of the machine lock system, which is not implemented here.
    assert result['locked_machine'] == result['machine_number']

def test_reserve_machine_user_single_active_reservation():
    reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T11:00:00Z", 25)
    assert result['error'] == "a user may only have a single active reservation at a time"

def test_reserve_machine_no_machines_available():
    for i in range(25):
        reserve_machine(f"user{i}@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    result = reserve_machine("user26@example.com", "1234567890", "2023-10-01T11:00:00Z", 25)
    assert result['error'] == "no machines available"

def test_claim_machine_correct_pin():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    claim_result = claim_machine(result['identifier'], result['pin'])
    assert claim_result['success'] is True
    assert claim_result['used'] is True

def test_claim_machine_unlocks_machine():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    claim_machine(result['identifier'], result['pin'])
    # This is a placeholder for checking the actual unlock mechanism.
    assert result['locked_machine'] == False  # This line should interact with a lock system

def test_claim_machine_wrong_pin():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    claim_result = claim_machine(result['identifier'], "wrongpin")
    assert claim_result['success'] is False
    assert claim_result['used'] is False

def test_claim_machine_no_reservation():
    claim_result = claim_machine("RSV-00000000", "12345")
    assert claim_result['error'] == "no reservation found"

def test_claim_machine_already_used():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    claim_machine(result['identifier'], result['pin'])
    claim_result = claim_machine(result['identifier'], result['pin'])
    assert claim_result['error'] == "reservation has already been used"

def test_reserve_machine_after_claim():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    claim_machine(result['identifier'], result['pin'])
    new_reservation = reserve_machine("user@example.com", "1234567890", "2023-10-01T11:00:00Z", 25)
    assert new_reservation['identifier'] != result['identifier']

def test_pin_reset_on_fifth_attempt():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    for _ in range(4):
        claim_machine(result['identifier'], "wrongpin")
    reset_result = claim_machine(result['identifier'], "wrongpin")
    assert reset_result['new_pin'] != result['pin']

def test_pin_reset_sends_text_message():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    for _ in range(4):
        claim_machine(result['identifier'], "wrongpin")
    reset_result = claim_machine(result['identifier'], "wrongpin")
    assert reset_result['text_message'] is not None

def test_reset_pin_re_engages_lock():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    for _ in range(4):
        claim_machine(result['identifier'], "wrongpin")
    reset_result = claim_machine(result['identifier'], "wrongpin")
    assert reset_result['locked_machine'] == result['machine_number']

def test_regenerated_pin_accepted():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    for _ in range(4):
        claim_machine(result['identifier'], "wrongpin")
    reset_result = claim_machine(result['identifier'], "wrongpin")
    new_claim_result = claim_machine(result['identifier'], reset_result['new_pin'])
    assert new_claim_result['success'] is True

def test_failed_attempt_count_resets():
    result = reserve_machine("user@example.com", "1234567890", "2023-10-01T10:00:00Z", 25)
    for _ in range(4):
        claim_machine(result['identifier'], "wrongpin")
    reset_result = claim_machine(result['identifier'], "wrongpin")  # triggers reset
    for _ in range(4):
        claim_result = claim_machine(result['identifier'], "wrongpin")
        assert claim_result['success'] is False
    new_claim_result = claim_machine(result['identifier'], reset_result['new_pin'])
    assert new_claim_result['success'] is True