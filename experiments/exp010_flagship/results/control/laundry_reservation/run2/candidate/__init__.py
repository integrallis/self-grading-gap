import random

class Reservation:
    def __init__(self, machine_number, pin, identifier, slot_time):
        self.machine_number = machine_number
        self.pin = pin
        self.identifier = identifier
        self.slot_time = slot_time
        self.is_active = True

class ClaimResult:
    def __init__(self, success, machine_unlocked):
        self.success = success
        self.machine_unlocked = machine_unlocked

reservations = {}

# Function to seed a random number generator

def seed_random_source(seed):
    return random.Random(seed)


def reserve_machine(random_source, email, time_slot):
    if len([r for r in reservations.values() if r.slot_time == time_slot and r.is_active]) > 0:
        raise Exception("a user may only have a single active reservation at a time")

    available_machines = [i for i in range(1, 26) if i not in [r.machine_number for r in reservations.values() if r.is_active]]
    if not available_machines:
        raise Exception("no machines available")

    machine_number = random_source.choice(available_machines)
    pin = str(random_source.randint(10000, 99999))
    identifier = f"RSV-{random_source.getrandbits(32):08X}"[:12]
    reservation = Reservation(machine_number, pin, identifier, time_slot)
    reservations[identifier] = reservation
    return reservation


def claim_machine(identifier, pin):
    if identifier not in reservations:
        raise Exception("Claiming a machine that has no reservation is rejected")

    reservation = reservations[identifier]
    if reservation.pin != pin:
        return ClaimResult(False, False)
    
    reservation.is_active = False
    return ClaimResult(True, True)


def reset_pin(identifier):
    if identifier not in reservations:
        raise Exception("Claiming a machine that has no reservation is rejected")

    reservation = reservations[identifier]
    new_pin = str(random.randint(10000, 99999))
    reservation.pin = new_pin
    return new_pin
