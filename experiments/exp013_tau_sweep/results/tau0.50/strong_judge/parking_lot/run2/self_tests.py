import pytest
from solution import ParkingLot

def test_configure_lot_with_valid_configuration():
    lot = ParkingLot()
    lot.configure({"motorcycle": 10, "compact": 20, "large": 30}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    # Expect no exceptions for valid configuration

def test_configure_lot_with_negative_spot_count():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure({"motorcycle": 10, "compact": -1, "large": 30}, 
                       {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configure_lot_with_no_spots():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure({"motorcycle": 0, "compact": 0, "large": 0}, 
                       {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configure_lot_with_missing_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                       {"motorcycle": 1.0, "car": 2.0})
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configure_lot_with_non_positive_hourly_rate():
    lot = ParkingLot()
    with pytest.raises(ValueError) as excinfo:
        lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                       {"motorcycle": 0.0, "car": 2.0, "bus": 5.0})
    assert str(excinfo.value) == "hourly rate for [motorcycle] must be positive, got [0.0]"

def test_motorcycle_parking():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "motorcycle"

def test_motorcycle_assignment_fallback():
    lot = ParkingLot()
    lot.configure({"motorcycle": 0, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-2", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "M-2"
    assert ticket["spot_type"] == "compact"

def test_car_parking():
    lot = ParkingLot()
    lot.configure({"motorcycle": 0, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("C-1", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "compact"

def test_car_assignment_to_large_spot():
    lot = ParkingLot()
    lot.configure({"motorcycle": 0, "compact": 0, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("C-2", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "C-2"
    assert ticket["spot_type"] == "large"

def test_car_turns_away_when_only_motorcycle_spots_available():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 0, "large": 0}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)  # Park a motorcycle
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", 1.0)  # Assume entry time is 1.0
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_turns_away_when_no_large_spots():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 0}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-1", 1.0)  # Assume entry time is 1.0
    assert str(excinfo.value) == "no available spot for [bus]"

def test_full_lot_check_in_fails():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)
    lot.check_in("C-1", 1.0)
    lot.check_in("B-1", 1.0)
    with pytest.raises(ValueError):
        lot.check_in("C-2", 1.0)  # Attempt to park another car

def test_checkout_vehicle_not_in_lot():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("ghost", 1.0)  # Assume entry time is 1.0
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_checkout_vehicle_and_free_spot():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", 1.0)
    lot.check_out("M-1", 2.0)  # Exit after 1 hour
    ticket = lot.check_in("C-1", 2.0)  # New check-in should succeed
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "compact"

def test_billing_minimum_charge():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", 1.0)  # Assume entry time is 1.0
    receipt = lot.check_out("M-1", 1.0)  # Exit after 0 hours
    assert receipt["fee"] == 1.0  # 1 hour minimum charge

def test_billing_partial_hours():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", 1.0)  # Assume entry time is 1.0
    receipt = lot.check_out("M-1", 2.5)  # Exit after 1.5 hours
    assert receipt["fee"] == 2.0  # 2 hours billed

def test_billing_exact_hours():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-1", 1.0)  # Assume entry time is 1.0
    receipt = lot.check_out("M-1", 4.0)  # Exit after 3 hours
    assert receipt["fee"] == 3.0  # 3 hours billed

def test_exit_time_before_entry_time():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 2.0)  # Assume entry time is 2.0
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("M-1", 1.0)  # Exit before check-in time
    assert str(excinfo.value) == "exit_time [1.0] is before entry_time [2.0]"

def test_report_occupancy():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["capacity"] == 1
    assert occupancy["motorcycle"]["occupied"] == 1
    assert occupancy["motorcycle"]["available"] == 0
    assert occupancy["compact"]["capacity"] == 1
    assert occupancy["compact"]["occupied"] == 0
    assert occupancy["compact"]["available"] == 1
    assert occupancy["large"]["capacity"] == 1
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 1

def test_occupancy_increases_after_checkout():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)
    lot.check_out("M-1", 2.0)  # Exit after 1 hour
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["available"] == 1  # Should increase available count for motorcycle

def test_motorcycle_assignment_to_large_spot_when_compact_full():
    lot = ParkingLot()
    lot.configure({"motorcycle": 0, "compact": 0, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("M-3", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "M-3"
    assert ticket["spot_type"] == "large"

def test_successful_bus_parking():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    ticket = lot.check_in("B-1", 1.0)  # Assume entry time is 1.0
    assert ticket["vehicle_id"] == "B-1"
    assert ticket["spot_type"] == "large"

def test_duplicate_check_in():
    lot = ParkingLot()
    lot.configure({"motorcycle": 1, "compact": 1, "large": 1}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)  # Park a motorcycle
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("M-1", 2.0)  # Attempt to park again
    assert str(excinfo.value) == "vehicle [M-1] is already parked"

def test_independent_checkout_of_same_type():
    lot = ParkingLot()
    lot.configure({"motorcycle": 2, "compact": 2, "large": 2}, 
                   {"motorcycle": 1.0, "car": 2.0, "bus": 5.0})
    lot.check_in("M-1", 1.0)
    lot.check_in("M-2", 1.0)
    lot.check_out("M-1", 2.0)  # Exit first motorcycle
    ticket = lot.check_in("M-3", 2.0)  # New check-in should succeed
    assert ticket["vehicle_id"] == "M-3"
    assert ticket["spot_type"] == "motorcycle"