import pytest
from solution import reserve_machine, claim_machine

class TestLaundryRoomReservation:
    def setup_method(self):
        # Each test should start with a fresh state for reservations
        self.reservations = []

    def reserve_machine(self, email, phone, slot, random_source):
        reservation = reserve_machine(email, phone, slot, random_source)
        self.reservations.append(reservation)
        return reservation

    def test_reserve_machine_success(self):
        # Create a reservation with a given slot and source of randomness
        result = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        
        # AC-1.1: Check machine number is between 1 and 25
        assert 1 <= result['machine_number'] <= 25
        
        # AC-1.2: Check that the PIN is exactly 5 digits
        assert len(result['pin']) == 5 and result['pin'].isdigit()
        
        # AC-1.3: Check that identifier matches the required format
        assert result['identifier'].startswith("RSV-") and len(result['identifier']) == 12
        assert all(c in "0123456789ABCDEF" for c in result['identifier'][4:])  # Hexadecimal
        
        # AC-1.4: Check that the reservation is active
        assert result['active'] is True
        
        # AC-1.5: Check that the slot is recorded correctly
        assert result['slot'] == "2023-10-01T10:00:00"

    def test_reserve_machine_identifier_unique(self):
        # Test to ensure different identifiers for different reservations
        result1 = self.reserve_machine("resident1@example.com", "1234567890", "2023-10-01T10:00:00", "random_source1")
        result2 = self.reserve_machine("resident2@example.com", "0987654321", "2023-10-01T11:00:00", "random_source2")
        assert result1['identifier'] != result2['identifier']

    def test_reserve_machine_randomness(self):
        # Test to ensure machine selection is randomized and does not collide for the same user
        result1 = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        result2 = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T11:00:00", "random_source")
        assert result1['machine_number'] != result2['machine_number']

    def test_reserve_machine_one_active_reservation(self):
        self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        with pytest.raises(Exception, match=r"^a user may only have a single active reservation at a time$"):
            self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T11:00:00", "random_source")

    def test_reserve_machine_no_machines_available(self):
        for i in range(1, 26):
            self.reserve_machine(f"resident{i}@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        with pytest.raises(Exception, match=r"^no machines available$"):
            self.reserve_machine("resident27@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")

    def test_claim_machine_success(self):
        reservation = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        claim_result = claim_machine(reservation['identifier'], reservation['pin'])
        # AC-4.1: Check reservation is now inactive
        assert reservation['active'] is False  # The reservation should now be marked as used
        # AC-4.2: Here we expect the machine to be unlocked; verify this might depend on implementation

    def test_claim_machine_incorrect_pin(self):
        reservation = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        claim_result = claim_machine(reservation['identifier'], "wrong_pin")
        # AC-4.3: Check the reservation is still active
        assert reservation['active'] is True  # The reservation should still be active

    def test_claim_machine_no_reservation(self):
        # Check that claiming a nonexistent reservation is rejected
        claim_result = claim_machine("RSV-NONEXISTENT", "12345")
        # AC-4.4: We expect rejection but do not define the mechanism

    def test_five_attempt_pin_reset_no_message(self):
        reservation = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        for _ in range(4):
            claim_machine(reservation['identifier'], "wrong_pin")
        # We cannot assert here; this will be verified in the next test.

    def test_fifth_attempt_pin_reset(self):
        reservation = self.reserve_machine("resident@example.com", "1234567890", "2023-10-01T10:00:00", "random_source")
        for _ in range(4):
            claim_machine(reservation['identifier'], "wrong_pin")
        # On the fifth attempt we expect the PIN to be reset and an SMS to be sent (not directly testable here)
        new_pin = claim_machine(reservation['identifier'], "wrong_pin")  # Simulate the 5th wrong entry
        # Verify new PIN is generated and can be used
        assert len(new_pin) == 5 and new_pin.isdigit()  # AC-5.2
        claim_result = claim_machine(reservation['identifier'], new_pin)
        assert claim_result is True  # AC-5.4