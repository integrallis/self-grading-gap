from solution import ParkingLot

def test_configuring_lot_with_negative_spot_count():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={'motorcycle': -1, 'compact': 2, 'large': 3}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert str(excinfo.value) == "spot count for [motorcycle] must be non-negative, got [-1]"

def test_configuring_lot_with_no_spots():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={'motorcycle': 0, 'compact': 0, 'large': 0}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    assert str(excinfo.value) == "parking lot must have at least one spot"

def test_configuring_lot_with_missing_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={'motorcycle': 1, 'compact': 2, 'large': 3}, rates={'motorcycle': 1.0, 'car': 2.0})
    assert str(excinfo.value) == "missing hourly rate for [bus]"

def test_configuring_lot_with_non_positive_hourly_rate():
    with pytest.raises(ValueError) as excinfo:
        ParkingLot(spots={'motorcycle': 1, 'compact': 2, 'large': 3}, rates={'motorcycle': 1.0, 'car': 0.0, 'bus': 5.0})
    assert str(excinfo.value) == "hourly rate for [car] must be positive, got [0.0]"

def test_motorcycle_parks_in_motorcycle_spot():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 2, 'large': 3}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    ticket = lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    assert ticket['spot_type'] == 'motorcycle'

def test_car_parks_in_compact_spot():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 1, 'large': 3}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    ticket = lot.check_in(vehicle_id='C-1', vehicle_type='car', entry_time=1001.0)
    assert ticket['spot_type'] == 'compact'

def test_bus_parks_in_large_spot():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in(vehicle_id='C-1', vehicle_type='car', entry_time=1000.0)
    ticket = lot.check_in(vehicle_id='B-1', vehicle_type='bus', entry_time=1001.0)
    assert ticket['spot_type'] == 'large'

def test_car_turns_away_when_no_compact_spots():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 0, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in(vehicle_id='C-1', vehicle_type='car', entry_time=1000.0)
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id='C-2', vehicle_type='car', entry_time=1001.0)
    assert str(excinfo.value) == "no available spot for [car]"

def test_bus_turns_away_when_no_large_spots():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 1, 'large': 0}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_in(vehicle_id='B-1', vehicle_type='bus', entry_time=1000.0)
    assert str(excinfo.value) == "no available spot for [bus]"

def test_checking_out_vehicle_frees_spot():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    lot.check_out(vehicle_id='M-1', exit_time=1100.0)
    assert lot.occupancy()['motorcycle']['available'] == 1

def test_checking_out_non_parked_vehicle():
    lot = ParkingLot(spots={'motorcycle': 1, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    with pytest.raises(ValueError) as excinfo:
        lot.check_out(vehicle_id='ghost', exit_time=1100.0)
    assert str(excinfo.value) == "vehicle [ghost] is not parked"

def test_billing_for_zero_length_stay():
    lot = ParkingLot(spots={'motorcycle': 1}, rates={'motorcycle': 1.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    receipt = lot.check_out(vehicle_id='M-1', exit_time=1000.0)
    assert receipt['billed_hours'] == 1
    assert receipt['fee'] == 1.0  # 1 hour * 1.0 per hour

def test_billing_for_partial_hours():
    lot = ParkingLot(spots={'motorcycle': 1}, rates={'motorcycle': 1.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    receipt = lot.check_out(vehicle_id='M-1', exit_time=1090.0)  # 90 minutes
    assert receipt['billed_hours'] == 2
    assert receipt['fee'] == 2.0  # 2 hours * 1.0 per hour

def test_billing_for_exact_hours():
    lot = ParkingLot(spots={'motorcycle': 1}, rates={'motorcycle': 1.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    receipt = lot.check_out(vehicle_id='M-1', exit_time=1300.0)  # 3 hours
    assert receipt['billed_hours'] == 3
    assert receipt['fee'] == 3.0  # 3 hours * 1.0 per hour

def test_receipt_records_details():
    lot = ParkingLot(spots={'motorcycle': 1}, rates={'motorcycle': 1.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    receipt = lot.check_out(vehicle_id='M-1', exit_time=1200.0)
    assert receipt['vehicle_id'] == 'M-1'
    assert receipt['vehicle_type'] == 'motorcycle'
    assert receipt['spot_type'] == 'motorcycle'
    assert receipt['entry_time'] == 1000.0
    assert receipt['exit_time'] == 1200.0
    assert receipt['billed_hours'] == 1
    assert receipt['fee'] == 1.0

def test_occupancy_reporting():
    lot = ParkingLot(spots={'motorcycle': 2, 'compact': 1, 'large': 1}, rates={'motorcycle': 1.0, 'car': 2.0, 'bus': 5.0})
    lot.check_in(vehicle_id='M-1', vehicle_type='motorcycle', entry_time=1000.0)
    lot.check_in(vehicle_id='C-1', vehicle_type='car', entry_time=1001.0)
    occupancy = lot.occupancy()
    assert occupancy['motorcycle']['occupied'] == 1
    assert occupancy['motorcycle']['available'] == 1
    assert occupancy['compact']['occupied'] == 1
    assert occupancy['compact']['available'] == 0
    assert occupancy['large']['occupied'] == 0
    assert occupancy['large']['available'] == 1