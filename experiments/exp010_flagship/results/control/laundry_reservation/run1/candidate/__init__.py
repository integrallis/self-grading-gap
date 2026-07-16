import random
import string

reservations = {}

MACHINE_COUNT = 25

class Reservation:
    def __init__(self, machine_number, pin, identifier, email, time_slot):
        self.machine_number = machine_number
        self.pin = pin
        self.identifier = identifier
        self.email = email
        self.time_slot = time_slot
        self.active = True
        self.attempts = 0
        self.text_message_sent = False

    def claim(self, pin):
        if not self.active:
            raise Exception('Claiming a machine that has no reservation is rejected')
        if pin == self.pin:
            self.active = False
            return {'success': True}
        else:
            self.attempts += 1
            if self.attempts >= 5:
                self.reset_pin()
            return {'success': False}

    def reset_pin(self):
        self.pin = random.randint(10000, 99999)
        self.attempts = 0
        self.text_message_sent = True


def reserve_machine(random_source, email, time_slot):
    if len(reservations) >= MACHINE_COUNT:
        raise Exception('no machines available')
    for res in reservations.values():
        if res.email == email and res.active:
            raise Exception('a user may only have a single active reservation at a time')
    machine_number = random_source.randint(1, MACHINE_COUNT)
    pin = random_source.randint(10000, 99999)
    identifier = 'RSV-' + ''.join(random_source.choices(string.hexdigits.lower(), k=8))
    reservation = Reservation(machine_number, pin, identifier, email, time_slot)
    reservations[identifier] = reservation
    return {'machine_number': machine_number, 'pin': pin, 'identifier': identifier, 'active': True, 'time_slot': time_slot}


def claim_machine(identifier, pin):
    if identifier not in reservations:
        raise Exception('Claiming a machine that has no reservation is rejected')
    reservation = reservations[identifier]
    return reservation.claim(pin)


def reset_pin(identifier):
    if identifier not in reservations:
        raise Exception('Claiming a machine that has no reservation is rejected')
    reservation = reservations[identifier]
    reservation.reset_pin()