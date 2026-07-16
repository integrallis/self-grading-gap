class ParkingLot:
    def __init__(self):
        self.spots = {}
        self.rates = {}
        self.parked_vehicles = {}

    def configure(self, spots, rates):
        if not any(spots.values()):
            raise ValueError("parking lot must have at least one spot")
        for spot_type, count in spots.items():
            if count < 0:
                raise ValueError(f"spot count for [{spot_type}] must be non-negative, got [{count}]")
        self.spots = spots
        for rate_type, rate in rates.items():
            if rate <= 0:
                raise ValueError(f"hourly rate for [{rate_type}] must be positive, got [{rate}]")
            if rate_type not in spots:
                raise ValueError(f"missing hourly rate for [{rate_type}]")
        self.rates = rates
        self.parked_vehicles = {}

    def check_in(self, vehicle_id, vehicle_type, entry_time):
        if vehicle_type not in self.spots or self.spots[vehicle_type] <= 0:
            raise ValueError(f"no available spot for [{vehicle_type}]")
        self.spots[vehicle_type] -= 1
        self.parked_vehicles[vehicle_id] = (vehicle_type, entry_time)
        return {"vehicle_id": vehicle_id, "spot_type": vehicle_type}

    def check_out(self, vehicle_id, exit_time):
        if vehicle_id not in self.parked_vehicles:
            raise ValueError(f"vehicle [{vehicle_id}] is not parked")
        vehicle_type, entry_time = self.parked_vehicles.pop(vehicle_id)
        if exit_time < entry_time:
            raise ValueError(f"exit_time [{exit_time}] is before entry_time [{entry_time}]")
        billed_hours = (exit_time - entry_time) // 100
        fee = billed_hours * self.rates[vehicle_type]
        self.spots[vehicle_type] += 1
        return {"billed_hours": billed_hours, "fee": fee}

    def is_parked(self, vehicle_id):
        return vehicle_id in self.parked_vehicles

    def get_occupancy(self):
        occupancy = {}
        for spot_type, capacity in self.spots.items():
            occupied = sum(1 for v in self.parked_vehicles.values() if v[0] == spot_type)
            occupancy[spot_type] = {
                "capacity": capacity,
                "occupied": occupied,
                "available": capacity - occupied
            }
        return occupancy