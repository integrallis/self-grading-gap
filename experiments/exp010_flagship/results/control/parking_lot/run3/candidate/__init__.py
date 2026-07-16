import pytest

class ParkingLot:
    def __init__(self, spots, rates):
        self.spots = spots
        self.rates = rates
        self.parked_vehicles = {}
        self.validate_configuration()

    def validate_configuration(self):
        if not any(self.spots.values()):
            raise ValueError("parking lot must have at least one spot")
        for vehicle_type, count in self.spots.items():
            if count < 0:
                raise ValueError(f"spot count for [{vehicle_type}] must be non-negative, got [{count}]")
        for vehicle_type in self.spots.keys():
            if vehicle_type not in self.rates:
                raise ValueError(f"missing hourly rate for [{vehicle_type}]")
            if self.rates[vehicle_type] <= 0:
                raise ValueError(f"hourly rate for [{vehicle_type}] must be positive, got [{self.rates[vehicle_type]}]")

    def check_in(self, vehicle_id, vehicle_type, entry_time):
        if vehicle_id in self.parked_vehicles:
            raise ValueError(f"vehicle [{vehicle_id}] is already parked")
        if self.spots.get(vehicle_type, 0) <= 0:
            raise ValueError(f"no available spot for [{vehicle_type}]")
        self.spots[vehicle_type] -= 1
        self.parked_vehicles[vehicle_id] = {'type': vehicle_type, 'entry_time': entry_time}
        return {'spot_type': vehicle_type}

    def check_out(self, vehicle_id, exit_time):
        if vehicle_id not in self.parked_vehicles:
            raise ValueError(f"vehicle [{vehicle_id}] is not parked")
        vehicle_info = self.parked_vehicles.pop(vehicle_id)
        vehicle_type = vehicle_info['type']
        entry_time = vehicle_info['entry_time']
        billed_hours = max(1, (exit_time - entry_time + 59) // 60)
        fee = billed_hours * self.rates[vehicle_type]
        self.spots[vehicle_type] += 1
        return {
            'vehicle_id': vehicle_id,
            'vehicle_type': vehicle_type,
            'spot_type': vehicle_type,
            'entry_time': entry_time,
            'exit_time': exit_time,
            'billed_hours': billed_hours,
            'fee': fee
        }

    def occupancy(self):
        return {vehicle_type: {'occupied': sum(1 for v in self.parked_vehicles.values() if v['type'] == vehicle_type), 'available': self.spots[vehicle_type]} for vehicle_type in self.spots}