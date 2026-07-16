import pytest
from solution import ParkingLot

# US-1: Configuring the lot
def test_configure_parking_lot_with_valid_configuration():
    lot = ParkingLot(10, 20, 5, 1.0, 2.0, 5.0)
    assert lot is not None

def test_configure_parking_lot_with_negative_motorcycle_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(-1, 20, 5, 1.0, 2.0, 5.0)
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_configure_parking_lot_with_negative_compact_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(1, -1, 5, 1.0, 2.0, 5.0)
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_configure_parking_lot_with_negative_large_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(1, 1, -1, 1.0, 2.0, 5.0)
    assert str(excinfo.value) == "spot count for [large] must be non-negative, got [-1]"

def test_configure_parking_lot_with_no_spots():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(0, 0, 0, 1.0, 2.0, 5.0)
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configure_parking_lot_with_missing_motorcycle_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, None, 2.0, 5.0)
    assert str(excinfo.value) == "missing hourly rate for [motorcycle]"

def test_configure_parking_lot_with_missing_car_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, None, 5.0)
    assert str(excinfo.value) == "missing hourly rate for [car]"

def test_configure_parking_lot_with_missing_bus_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, 2.0, None)
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configure_parking_lot_with_non_positive_motorcycle_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 0.0, 2.0, 5.0)
    assert str(excinfo.value) == "hourly rate for [motorcycle] must be positive, got [0.0]"

def test_configure_parking_lot_with_non_positive_car_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, 0.0, 5.0)
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_configure_parking_lot_with_non_positive_bus_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, 2.0, 0.0)
    assert str(excinfo.value) == "hourly rate for [bus] must be positive, got [0.0]"

def test_configure_parking_lot_with_negative_motorcycle_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, -1.0, 2.0, 5.0)
    assert str(excinfo.value) == "hourly rate for [motorcycle] must be positive, got [-1.0]"

def test_configure_parking_lot_with_negative_car_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, -2.0, 5.0)
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [-2.0]"

def test_configure_parking_lot_with_negative_bus_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(10, 20, 5, 1.0, 2.0, -5.0)
    assert str(excinfo.value) == "hourly rate for [bus] must be positive, got [-5.0]"

# US-2: Assigning spots on arrival
def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "motorcycle"

def test_motorcycle_parks_in_compact_spot_when_motorcycle_spot_full():
    lot = ParkingLot(0, 1, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "compact"

def test_motorcycle_parks_in_large_spot_when_compact_spot_full():
    lot = ParkingLot(0, 0, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket["vehicle_id"] == "M-1"
    assert ticket["spot_type"] == "large"

def test_car_parks_in_compact_spot():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "compact"

def test_car_parks_in_large_spot_when_compact_spot_full():
    lot = ParkingLot(0, 1, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    assert ticket["vehicle_id"] == "C-1"
    assert ticket["spot_type"] == "large"

def test_car_rejects_motorcycle_spot():
    lot = ParkingLot(1, 0, 0, 1.0, 2.0, 5.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1000.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_parks_in_large_spot():
    lot = ParkingLot(0, 0, 1, 1.0, 2.0, 5.0)
    ticket = lot.check_in("B-1", "bus", 1000.0)
    assert ticket["vehicle_id"] == "B-1"
    assert ticket["spot_type"] == "large"

def test_bus_rejects_when_no_large_spots():
    lot = ParkingLot(0, 1, 0, 1.0, 2.0, 5.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-1", "bus", 1000.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_check_in_fails_when_full():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_in("B-1", "bus", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-2", "car", 1000.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_check_in_twice_fails():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1000.0)
    assert str(excinfo.value) == "vehicle [C-1] is already parked"

def test_vehicle_reported_as_parked_after_check_in():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    assert lot.is_parked("C-1") is True

def test_check_out_frees_spot():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # 1 hour later
    assert not lot.is_parked("C-1")

def test_check_out_non_existent_vehicle_fails():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("ghost", 1100.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_multiple_vehicles_checkout_independently():
    lot = ParkingLot(2, 2, 2, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_in("C-2", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # 1 hour later
    lot.check_out("C-2", 1200.0)  # 2 hours later
    assert not lot.is_parked("C-1")
    assert not lot.is_parked("C-2")

def test_check_out_and_check_in_another_vehicle():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # 1 hour later
    ticket = lot.check_in("C-2", "car", 1200.0)  # Check in another car
    assert ticket["vehicle_id"] == "C-2"
    assert ticket["spot_type"] == "compact"

# US-4: Billing the stay
def test_billing_minimum_charge():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1000.0)  # Same time
    assert receipt['billed_hours'] == 1
    assert receipt['fee'] == 1.0  # 1 hour * 1.0 rate

def test_billing_ten_minutes_stay():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1010.0)  # 10 minutes later
    assert receipt['billed_hours'] == 1
    assert receipt['fee'] == 1.0  # 1 hour * 1.0 rate

def test_billing_partial_hours_round_up():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1090.0)  # 90 minutes later
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0  # 2 hours * 1.0 rate

def test_billing_one_second_past_hour():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 3601.0)  # 1 hour and 1 second later
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0  # 2 hours * 1.0 rate

def test_billing_exact_hours_no_round_up():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1200.0)  # 2 hours later
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0  # 2 hours * 1.0 rate

def test_billing_exact_three_hours():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 4000.0)  # 3 hours later
    assert receipt['billed_hours'] == 3
    assert receipt['fee'] == 3.0  # 3 hours * 1.0 rate

def test_billing_two_hour_for_car():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1200.0)  # 2 hours later
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 4.0  # 2 hours * 2.0 rate

def test_billing_two_hour_for_bus():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("B-1", "bus", 1000.0)
    receipt = lot.check_out("B-1", 1200.0)  # 2 hours later
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 10.0  # 2 hours * 5.0 rate

def test_billing_receipt_details():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    receipt = lot.check_out("M-1", 1200.0)  # 2 hours later
    assert receipt['vehicle_id'] == "M-1"
    assert receipt['vehicle_type'] == "motorcycle"
    assert receipt['spot_type'] == "motorcycle"
    assert receipt['entry_time'] == 1000.0
    assert receipt['exit_time'] == 1200.0
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0

def test_exit_time_before_entry_time_fails():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("M-1", 999.0)
    assert str(excinfo.value) == "exit_time [999.0] is before entry_time [1000.0]"

# US-5: Reporting occupancy
def test_report_occupancy():
    lot = ParkingLot(2, 2, 2, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    occupancy = lot.report_occupancy()
    assert occupancy["motorcycle"]["capacity"] == 2
    assert occupancy["motorcycle"]["occupied"] == 0
    assert occupancy["motorcycle"]["available"] == 2
    assert occupancy["compact"]["capacity"] == 2
    assert occupancy["compact"]["occupied"] == 1
    assert occupancy["compact"]["available"] == 1
    assert occupancy["large"]["capacity"] == 2
    assert occupancy["large"]["occupied"] == 0
    assert occupancy["large"]["available"] == 2

def test_report_occupancy_after_check_out():
    lot = ParkingLot(1, 1, 1, 1.0, 2.0, 5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # 1 hour later
    occupancy = lot.report_occupancy()
    assert occupancy["compact"]["occupied"] == 0
    assert occupancy["compact"]["available"] == 1