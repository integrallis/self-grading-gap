# file: laundry_reservation.py
from candidate import Reservation as Reservation
from candidate import claim_machine as claim_reservation
from candidate import reserve_machine as create_reservation
from candidate import reservations

ReservationError = Exception
get_reservation = reservations.get


class MachineApi:
    def __init__(self, random_source):
        self.random_source = random_source

    def create_reservation(self, email, time_slot):
        return create_reservation(self.random_source, email, time_slot)

    def claim_reservation(self, identifier, pin):
        return claim_reservation(identifier, pin)

    def get_reservation(self, identifier):
        return get_reservation(identifier)


class LaundryService:
    def __init__(self, machine_api, reservation_store, notifier, clock):
        self.machine_api = machine_api
        self.reservation_store = reservation_store
        self.notifier = notifier
        self.clock = clock

    def create_reservation(self, email, time_slot):
        return self.machine_api.create_reservation(email, time_slot)

    def claim_reservation(self, identifier, pin):
        return self.machine_api.claim_reservation(identifier, pin)

    def get_reservation(self, identifier):
        return self.machine_api.get_reservation(identifier)
