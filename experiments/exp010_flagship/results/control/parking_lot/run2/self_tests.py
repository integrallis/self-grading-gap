# test_parking_lot.py

from solution import ParkingLot

def test_configure_parking_lot_with_valid_configuration():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 5, "compact": 10, "large": 15},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert lot.spots == {"motorcycle": 5, "compact": 10, "large": 15}
    assert lot.rates == {"motorcycle": 1.0, "car": 2.0, "bus": 5.0}

def test_configure_parking_lot_with_negative_spot_count():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure(spots={"motorcycle": -1, "compact": 10, "large": 15},
                      rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_configure_parking_lot_with_zero_spots():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure(spots={"motorcycle": 0, "compact": 0, "large": 0},
                      rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configure_parking_lot_with_missing_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure(spots={"motorcycle": 5, "compact": 10, "large": 15},
                      rates={"motorcycle": 1.0, "car": 2.0})  # Missing rate for bus
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configure_parking_lot_with_non_positive_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure(spots={"motorcycle": 5, "compact": 10, "large": 15},
                      rates={"motorcycle": 1.0, "car": 0.0, "bus": 5.0})  # Non-positive rate for car
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "motorcycle"

def test_car_parks_in_compact_spot():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 0, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("C-1", "car", 1000.0)
    assert ticket['vehicle_id'] == "C-1"
    assert ticket['spot_type'] == "compact"

def test_bus_parks_in_large_spot():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 0, "compact": 0, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("B-1", "bus", 1000.0)
    assert ticket['vehicle_id'] == "B-1"
    assert ticket['spot_type'] == "large"

def test_no_available_spot_for_car():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 0, "compact": 0, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("B-1", "bus", 1000.0)  # Fill the large spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1000.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_no_available_spot_for_bus():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 0, "compact": 0, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("C-1", "car", 1000.0)  # Fill the large spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-1", "bus", 1000.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_checkout_vehicle():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # 1 hour stay
    assert not lot.is_parked("C-1")

def test_checkout_non_parked_vehicle():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("ghost", 1100.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_billing_for_stay():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1200.0)  # 2 hour stay
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0  # 2 hours * $1.0 per hour

def test_exit_time_before_entry_time():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 1, "large": 1},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("C-1", "car", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("C-1", 900.0)  # Exit time before entry time
    assert str(excinfo.value) == "exit_time [900.0] is before entry_time [1000.0]"

def test_parking_lot_occupancy_report():
    lot = ParkingLot()
    lot.configure(spots={"motorcycle": 1, "compact": 2, "large": 3},
                  rates={"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert lot.get_occupancy() == {
        "motorcycle": {"capacity": 1, "occupied": 0, "available": 1},
        "compact": {"capacity": 2, "occupied": 0, "available": 2},
        "large": {"capacity": 3, "occupied": 0, "available": 3},
    }
    lot.check_in("M-1", "motorcycle", 1000.0)
    assert lot.get_occupancy() == {
        "motorcycle": {"capacity": 1, "occupied": 1, "available": 0},
        "compact": {"capacity": 2, "occupied": 0, "available": 2},
        "large": {"capacity": 3, "occupied": 0, "available": 3},
    }