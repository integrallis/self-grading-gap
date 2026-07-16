# file: laundry_reservation.py
from candidate import ClaimResult
from candidate import Reservation
from candidate import claim_machine
from candidate import reservations
from candidate import reserve_machine


ReservationError = Exception


class MachineApi:
    def __init__(self, random_source):
        self.random_source = random_source

    def create_reservation(self, email, time_slot):
        return reserve_machine(self.random_source, email, time_slot)

    def claim_reservation(self, identifier, pin):
        return claim_machine(identifier, pin)

    def get_reservation(self, identifier):
        return reservations.get(identifier)


class LaundryService:
    def __init__(self, machine_api, random_source, clock, reservation_store):
        self.machine_api = machine_api
        self.random_source = random_source
        self.clock = clock
        self.reservation_store = reservation_store

    def create_reservation(self, random_source, email, time_slot):
        return reserve_machine(random_source, email, time_slot)

    def claim_reservation(self, identifier, pin):
        return claim_machine(identifier, pin)

    def get_reservation(self, identifier):
        return reservations.get(identifier)
