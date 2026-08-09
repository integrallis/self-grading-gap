import pytest
import re
from solution import reserve_machine, claim_machine, reset_pin

# A fresh seeded random source for each test
def create_seeded_random_source(seed):
    # Function to create a seeded random source (placeholder)
    pass

# Fixture to create a fresh reservation service and reset state
@pytest.fixture
def reservation_service():
    # Initialize the service with a fresh seeded random source
    return create_seeded_random_source(seed=42)

def test_reserve_machine_success(reservation_service):
    result = reserve_machine(
        user_id="user1",
        slot_time="2023-10-01T10:00:00",
        email="user1@example.com",
        phone="1234567890",
        random_source=reservation_service
    )
    assert 1 <= result['machine_number'] <= 25  # AC-1.1
    assert isinstance(result['pin'], str) and len(result['pin']) == 5 and result['pin'].isdigit()  # AC-1.2
    assert re.match(r'^RSV-[0-9A-F]{8}$', result['identifier'])  # AC-1.3
    assert result['slot_time'] == "2023-10-01T10:00:00"  # AC-1.5
    assert result['active'] is True  # AC-1.4

def test_reserve_machine_unique_identifiers(reservation_service):
    identifiers = set()
    for i in range(10):  # Create 10 reservations
        result = reserve_machine(
            user_id=f"user{i}",
            slot_time="2023-10-01T10:00:00",
            email=f"user{i}@example.com",
            phone="1234567890",
            random_source=reservation_service
        )
        identifiers.add(result['identifier'])
    assert len(identifiers) == 10  # No collisions should occur

def test_reserve_machine_no_machines_available(reservation_service):
    for i in range(25):
        reserve_machine(
            user_id=f"user{i}",
            slot_time="2023-10-01T10:00:00",
            email=f"user{i}@example.com",
            phone="1234567890",
            random_source=reservation_service
        )
    with pytest.raises(Exception) as excinfo:
        reserve_machine(
            user_id="user26",
            slot_time="2023-10-01T10:00:00",
            email="user26@example.com",
            phone="1234567890",
            random_source=reservation_service
        )
    assert str(excinfo.value) == "no machines available"  # AC-3.3

def test_claim_machine_success(reservation_service):
    reservation = reserve_machine(
        user_id="user1",
        slot_time="2023-10-01T10:00:00",
        email="user1@example.com",
        phone="1234567890",
        random_source=reservation_service
    )
    result = claim_machine(reservation['identifier'], reservation['pin'])
    assert result['accepted'] is True  # AC-4.1
    assert result['used'] is True  # Reservation should now be marked as used
    assert result['machine_unlocked'] is True  # Machine should be unlocked

def test_claim_machine_wrong_pin(reservation_service):
    reservation = reserve_machine(
        user_id="user1",
        slot_time="2023-10-01T10:00:00",
        email="user1@example.com",
        phone="1234567890",
        random_source=reservation_service
    )
    result = claim_machine(reservation['identifier'], "wrong_pin")
    assert result['accepted'] is False  # AC-4.3
    assert result['active'] is True  # Reservation should still be active
    assert result['pin'] == reservation['pin']  # PIN should remain unchanged

def test_claim_no_reservation(reservation_service):
    result = claim_machine("RSV-INVALID", "12345")
    assert result['accepted'] is False  # AC-4.4

def test_pin_reset(reservation_service):
    reservation = reserve_machine(
        user_id="user1",
        slot_time="2023-10-01T10:00:00",
        email="user1@example.com",
        phone="1234567890",
        random_source=reservation_service
    )
    for _ in range(4):
        claim_machine(reservation['identifier'], "wrong_pin")
    result = claim_machine(reservation['identifier'], "wrong_pin")  # 5th attempt
    assert isinstance(result['pin'], str) and len(result['pin']) == 5 and result['pin'].isdigit()  # AC-5.2

def test_pin_reset_successful_claim(reservation_service):
    reservation = reserve_machine(
        user_id="user1",
        slot_time="2023-10-01T10:00:00",
        email="user1@example.com",
        phone="1234567890",
        random_source=reservation_service
    )
    for _ in range(4):
        claim_machine(reservation['identifier'], "wrong_pin")
    new_result = claim_machine(reservation['identifier'], "wrong_pin")  # 5th attempt
    result = claim_machine(reservation['identifier'], new_result['pin'])  # Claim with new PIN
    assert result['accepted'] is True  # AC-5.4