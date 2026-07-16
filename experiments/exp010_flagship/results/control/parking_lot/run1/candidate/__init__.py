class ParkingLot:
    def __init__(self):
        self.spots = {
            "motorcycle": 0,
            "compact": 0,
            "large": 0
        }
        self.rates = {}
        self.parked_vehicles = {}

    def configure_lot(self, motorcycle_spots, compact_spots, large_spots, rates):
        if motorcycle_spots < 0:
            raise ValueError("spot count for [motorcycle] must be non-negative, got [" + str(motorcycle_spots) + "]")
        if compact_spots < 0:
            raise ValueError("spot count for [compact] must be non-negative, got [" + str(compact_spots) + "]")
        if large_spots < 0:
            raise ValueError("spot count for [large] must be non-negative, got [" + str(large_spots) + "]")
        if motorcycle_spots == 0 and compact_spots == 0 and large_spots == 0:
            raise ValueError("parking lot must have at least one spot")
        self.spots["motorcycle"] = motorcycle_spots
        self.spots["compact"] = compact_spots
        self.spots["large"] = large_spots
        for vehicle_type in ["motorcycle", "compact", "large", "car", "bus"]:
            if vehicle_type not in rates:
                raise ValueError("missing hourly rate for [" + vehicle_type + "]")
            if rates[vehicle_type] <= 0:
                raise ValueError("hourly rate for [" + vehicle_type + "] must be positive, got [" + str(rates[vehicle_type]) + "]")
        self.rates = rates

    def check_in(self, vehicle_id, vehicle_type, entry_time):
        if vehicle_id in self.parked_vehicles:
            raise ValueError("vehicle [" + vehicle_id + "] is already parked")
        if vehicle_type not in self.spots:
            raise ValueError("invalid vehicle type [" + vehicle_type + "]")
        if self.spots[vehicle_type] > 0:
            self.spots[vehicle_type] -= 1
            self.parked_vehicles[vehicle_id] = (vehicle_type, entry_time)
            return {"vehicle_id": vehicle_id, "spot_type": vehicle_type}
        else:
            raise ValueError("no available spot for [" + vehicle_type + "]")

    def check_out(self, vehicle_id, exit_time):
        if vehicle_id not in self.parked_vehicles:
            raise ValueError("vehicle [" + vehicle_id + "] is not parked")
        vehicle_type, entry_time = self.parked_vehicles.pop(vehicle_id)
        if exit_time < entry_time:
            raise ValueError("exit_time [" + str(exit_time) + "] is before entry_time [" + str(entry_time) + "]")
        billed_hours = (exit_time - entry_time) // 100
        fee = billed_hours * self.rates[vehicle_type]
        self.spots[vehicle_type] += 1
        return {"vehicle_id": vehicle_id, "billed_hours": billed_hours, "fee": fee}

    def report_occupancy(self):
        return {
            "motorcycle": {"available": self.spots["motorcycle"], "occupied": sum(1 for v in self.parked_vehicles.values() if v[0] == "motorcycle")},
            "compact": {"available": self.spots["compact"], "occupied": sum(1 for v in self.parked_vehicles.values() if v[0] == "compact")},
            "large": {"available": self.spots["large"], "occupied": sum(1 for v in self.parked_vehicles.values() if v[0] == "large")}
        }