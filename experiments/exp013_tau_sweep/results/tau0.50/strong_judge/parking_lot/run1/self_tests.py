import pytest
from solution import ParkingLot

def test_configuring_lot_with_valid_configuration():
    lot = ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    assert lot is not None  # Ensure the lot is created successfully

def test_negative_motorcycle_spot_count_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=-1, compact_spots=10, large_spots=10,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_negative_compact_spot_count_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=-1, large_spots=10,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "spot count for [compact] must be non-negative, got [-1]"

def test_negative_large_spot_count_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=10, large_spots=-1,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "spot count for [large] must be non-negative, got [-1]"

def test_no_spots_at_all_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=0, compact_spots=0, large_spots=0,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_missing_hourly_rate_for_motorcycle_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=None, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "missing hourly rate for [motorcycle]"

def test_missing_hourly_rate_for_car_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=1.0, car_rate=None, bus_rate=5.0)
    assert str(excinfo.value) == "missing hourly rate for [car]"

def test_missing_hourly_rate_for_bus_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=None)
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_negative_hourly_rate_for_motorcycle_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=-1.0, car_rate=2.0, bus_rate=5.0)
    assert str(excinfo.value) == "hourly rate for [motorcycle] must be positive, got [-1.0]"

def test_negative_hourly_rate_for_car_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=1.0, car_rate=-1.0, bus_rate=5.0)
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [-1.0]"

def test_negative_hourly_rate_for_bus_refused():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(motorcycle_spots=10, compact_spots=20, large_spots=30,
                   motorcycle_rate=1.0, car_rate=2.0, bus_rate=-1.0)
    assert str(excinfo.value) == "hourly rate for [bus] must be positive, got [-1.0]"

def test_assigning_motorcycle_to_motorcycle_spot():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "motorcycle"

def test_assigning_motorcycle_to_compact_spot():
    lot = ParkingLot(motorcycle_spots=0, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "compact"

def test_assigning_motorcycle_to_large_spot():
    lot = ParkingLot(motorcycle_spots=0, compact_spots=0, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("M-1", "motorcycle", 1000.0)
    assert ticket['vehicle_id'] == "M-1"
    assert ticket['spot_type'] == "large"

def test_motorcycle_fallback_to_compact_spot():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)  # occupy motorcycle spot
    ticket = lot.check_in("M-2", "motorcycle", 1100.0)  # should take compact spot
    assert ticket['vehicle_id'] == "M-2"
    assert ticket['spot_type'] == "compact"

def test_no_available_spot_for_car_when_motorcycle_spots_free():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=0, large_spots=0,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)  # occupy motorcycle spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1100.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_no_available_spot_for_bus_when_only_compact_and_motorcycle_free():
    lot = ParkingLot(motorcycle_spots=0, compact_spots=1, large_spots=0,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)  # occupy compact spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("B-1", "bus", 1100.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_no_available_spot_for_motorcycle_when_all_spots_full():
    lot = ParkingLot(motorcycle_spots=0, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)  # occupy compact spot
    lot.check_in("B-1", "bus", 1100.0)  # occupy large spot
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("M-1", "motorcycle", 1200.0)  # no spots available
    assert str(excinfo.value) == "no available spot for [motorcycle]"

def test_full_lot_report_when_all_spots_occupied():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("M-1", "motorcycle", 1000.0)
    lot.check_in("C-1", "car", 1100.0)
    lot.check_in("B-1", "bus", 1200.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['large']['occupied'] == 1

def test_checking_in_reports_vehicle_as_parked():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)
    assert lot.is_parked("C-1")

def test_checkout_frees_spot_for_new_arrival():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_out("C-1", 1100.0)  # free up spot
    ticket = lot.check_in("C-2", "car", 1200.0)  # should succeed
    assert ticket['vehicle_id'] == "C-2"

def test_billing_for_zero_duration_stay():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1000.0)  # 0 hours
    assert receipt['fee'] == 2.0  # 1 hour charge
    assert receipt['vehicle_id'] == "C-1"
    assert receipt['vehicle_type'] == "car"
    assert receipt['spot_type'] == "compact"  # assuming it took compact spot
    assert receipt['entry_time'] == 1000.0
    assert receipt['exit_time'] == 1000.0
    assert receipt['billed_hours'] == 1

def test_billing_for_ten_minutes_stay():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1010.0)  # 10 minutes
    assert receipt['fee'] == 2.0  # 1 hour charge
    assert receipt['billed_hours'] == 1

def test_billing_for_ninety_minutes_stay():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1180.0)  # 90 minutes
    assert receipt['fee'] == 4.0  # 2 hours charge
    assert receipt['billed_hours'] == 2

def test_billing_for_one_second_past_hour_stay():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1100.1)  # 1 hour + 1 second
    assert receipt['fee'] == 4.0  # 2 hours charge
    assert receipt['billed_hours'] == 2

def test_billing_for_exactly_three_hours_stay():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    ticket = lot.check_in("C-1", "car", 1000.0)
    receipt = lot.check_out("C-1", 1300.0)  # 3 hours
    assert receipt['fee'] == 6.0  # 3 hours charge
    assert receipt['billed_hours'] == 3

def test_exit_time_before_entry_time_refused():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1200.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_out("C-1", 1000.0)
    assert str(excinfo.value) == "exit_time [1000.0] is before entry_time [1200.0]"

def test_reporting_occupancy():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['capacity'] == 1
    assert occupancy['motorcycle']['occupied'] == 0
    assert occupancy['motorcycle']['available'] == 1
    assert occupancy['compact']['capacity'] == 1
    assert occupancy['compact']['occupied'] == 0
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 1
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 1
    
    lot.check_in("M-1", "motorcycle", 1000.0)
    occupancy = lot.get_occupancy()
    assert occupancy['motorcycle']['capacity'] == 1
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['motorcycle']['available'] == 0
    assert occupancy['compact']['capacity'] == 1
    assert occupancy['compact']['occupied'] == 0
    assert occupancy['compact']['available'] == 1
    assert occupancy['large']['capacity'] == 1
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 1

def test_duplicate_check_in():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in("C-1", "car", 1010.0)
    assert str(excinfo.value) == "vehicle [C-1] is already parked"

def test_multiple_same_type_vehicles_check_out_independently():
    lot = ParkingLot(motorcycle_spots=1, compact_spots=1, large_spots=1,
                     motorcycle_rate=1.0, car_rate=2.0, bus_rate=5.0)
    lot.check_in("C-1", "car", 1000.0)
    lot.check_in("C-2", "car", 1100.0)
    lot.check_out("C-1", 1200.0)  # 1 hour
    lot.check_out("C-2", 1300.0)  # 1 hour
    assert not lot.is_parked("C-1")
    assert not lot.is_parked("C-2")