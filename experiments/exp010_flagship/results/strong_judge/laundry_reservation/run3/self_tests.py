import pytest
from solution import reserve_machine, claim_machine, ReservationError

class MockRandom:
    def __init__(self, seed):
        self.seed = seed
        self.count = 0
    
    def randrange(self, start, end):
        # deterministic behavior based on seed
        return (self.seed + self.count) % (end - start) + start
    
    def random(self):
        return self.seed % 1.0

def test_reserve_machine_success():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    
    assert 1 <= reservation.machine_number <= 25  # AC-1.1
    assert len(reservation.pin) == 5               # AC-1.2
    assert reservation.pin.isdigit()                # AC-1.2
    assert reservation.identifier.startswith("RSV-") and len(reservation.identifier) == 12  # AC-1.3
    assert all(c in '0123456789ABCDEF' for c in reservation.identifier[4:])  # AC-1.3
    assert reservation.active                        # AC-1.4
    assert reservation.slot_time == "2023-10-15T10:00:00"  # AC-1.5

def test_reserve_machine_error_user_limit():
    random_source = MockRandom(seed=12345)
    reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    
    with pytest.raises(ReservationError, match=r"^a user may only have a single active reservation at a time$"):
        reserve_machine(random_source, "user@example.com", "2023-10-15T11:00:00", "user_1")

def test_reserve_machine_error_no_machines_available():
    random_source = MockRandom(seed=12345)
    for i in range(25):
        reserve_machine(random_source, f"user_{i}@example.com", "2023-10-15T10:00:00", f"user_{i}")

    with pytest.raises(ReservationError, match=r"^no machines available$"):
        reserve_machine(random_source, "user_26@example.com", "2023-10-15T10:00:00", "user_26")

def test_claim_machine_success():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    
    claim_result = claim_machine(reservation.identifier, reservation.pin)
    
    assert not reservation.active                    # AC-4.1, reservation is marked used
    # Check to confirm the machine is unlocked
    assert claim_result.success                      # AC-4.1

def test_claim_machine_fail_wrong_pin():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    
    claim_result = claim_machine(reservation.identifier, "wrong_pin")  # Using a guaranteed wrong PIN
    
    assert not claim_result.success                   # AC-4.3
    assert reservation.active                          # AC-4.3

def test_pin_reset():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    old_pin = reservation.pin
    
    for _ in range(4):
        claim_machine(reservation.identifier, "wrong_pin")
    
    claim_result = claim_machine(reservation.identifier, "wrong_pin")  # Fifth wrong attempt
    
    assert reservation.pin != old_pin                     # Reset PIN should not match old PIN
    assert reservation.pin.isdigit()                      # Ensure it's still a valid PIN

def test_successive_reservations():
    random_source1 = MockRandom(seed=12345)
    random_source2 = MockRandom(seed=12346)
    reservation1 = reserve_machine(random_source1, "user_1@example.com", "2023-10-15T10:00:00", "user_1")
    reservation2 = reserve_machine(random_source2, "user_2@example.com", "2023-10-15T11:00:00", "user_2")

    assert reservation1.machine_number != reservation2.machine_number  # AC-3.2, different machines

def test_full_pin_range():
    random_source = MockRandom(seed=12345)
    pins = set()
    for i in range(100):
        reservation = reserve_machine(random_source, f"user_{i}@example.com", "2023-10-15T10:00:00", f"user_{i}")
        pins.add(reservation.pin)
    assert len(pins) > 1  # Ensure there are multiple unique PINs

def test_deterministic_reservations():
    random_source1 = MockRandom(seed=42)
    random_source2 = MockRandom(seed=42)
    reservation1 = reserve_machine(random_source1, "user_1@example.com", "2023-10-15T10:00:00", "user_1")
    reservation2 = reserve_machine(random_source2, "user_1@example.com", "2023-10-15T10:00:00", "user_1")

    assert reservation1.machine_number == reservation2.machine_number  # Machines should be the same
    assert reservation1.pin == reservation2.pin                      # PINs should be the same
    assert reservation1.identifier == reservation2.identifier        # Identifiers should be the same

def test_claim_unreserved_machine():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")

    with pytest.raises(ReservationError, match=r"^no reservation found$"):
        claim_machine("RSV-UNRESERVED", "12345")  # Attempting to claim a non-existing reservation

def test_claim_used_reservation():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    claim_machine(reservation.identifier, reservation.pin)  # Claim the reservation

    with pytest.raises(ReservationError, match=r"^reservation has already been claimed$"):
        claim_machine(reservation.identifier, reservation.pin)  # Attempting to claim again

def test_reserve_after_claim():
    random_source = MockRandom(seed=12345)
    reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T10:00:00", "user_1")
    claim_machine(reservation.identifier, reservation.pin)

    new_reservation = reserve_machine(random_source, "user@example.com", "2023-10-15T11:00:00", "user_1")
    assert new_reservation.active                        # New reservation should be active
    assert new_reservation.identifier != reservation.identifier  # Ensure different identifiers